#!/usr/bin/env python3
import json
import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
import typer
from rich.console import Console
from rich.progress import Progress
from pathlib import Path
import shutil
import subprocess
import sys
# import pkg_resources

from lingora.plugins.base import TranslationPlugin
from lingora.plugins.registry import PluginRegistry
from sanic import Sanic, response
from sanic.response import json as sanic_json
import webbrowser
from functools import partial

app = typer.Typer()
console = Console()

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON file: {e}[/red]")
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(1)

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file with proper formatting."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        console.print(f"[red]Error saving file: {e}[/red]")
        raise typer.Exit(1)

def find_json_files(directory: str) -> list[Path]:
    """Find all JSON files in directory recursively."""
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(Path(root) / file)
    return json_files

def create_id_mapping(json_data: Dict[str, Any], counter: int = 1) -> tuple[Dict[str, Any], Dict[int, str], int]:
    """Create a mapping of strings to IDs and vice versa."""
    id_data = {}
    string_map = {}
    
    for key, value in json_data.items():
        if isinstance(value, str):
            id_data[key] = counter
            string_map[counter] = value
            counter += 1
        elif isinstance(value, dict):
            id_data[key], new_map, counter = create_id_mapping(value, counter)
            string_map.update(new_map)
    
    return id_data, string_map, counter

def generate_xml(json_files: list[Path], base_dir: Path) -> tuple[Path, Dict[Path, Dict[int, str]]]:
    """Generate XML file from JSON files with ID mappings."""
    root = ET.Element("uistrings")
    string_maps = {}
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    for json_file in json_files:
        relative_path = json_file.relative_to(base_dir)
        json_data = load_json_file(str(json_file))
        
        # Create folder nodes if needed
        current = root
        parts = relative_path.parent.parts
        for part in parts:
            folder = ET.SubElement(current, "folder", src=part)
            current = folder
        
        # Create file node
        file_node = ET.SubElement(current, "file", src=str(relative_path))
        
        # Generate ID mapping and save temporary JSON
        id_data, string_map, _ = create_id_mapping(json_data)
        string_maps[json_file] = string_map
        
        # Add string nodes to XML
        for id_num, text in string_map.items():
            string_node = ET.SubElement(file_node, "s", id=str(id_num))
            string_node.text = text
        
        # Save ID-mapped JSON
        tmp_json_path = tmp_dir / relative_path
        tmp_json_path.parent.mkdir(parents=True, exist_ok=True)
        save_json_file(id_data, str(tmp_json_path))
    
    # Save XML file
    xml_path = tmp_dir / "strings.xml"
    tree = ET.ElementTree(root)
    tree.write(str(xml_path), encoding="utf-8", xml_declaration=True)
    
    return xml_path, string_maps

def translate_xml(xml_path: Path, source_lang: str, target_lang: str, plugin: TranslationPlugin) -> Path:
    """Translate the XML file using the specified plugin."""
    # Read the entire XML file as a string
    with open(xml_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Send the entire XML content to the plugin for translation
    translated_xml = plugin.translate(xml_content, source_lang, target_lang)
    
    # Save the translated XML to a new file
    output_path = xml_path.parent / f"translated_{xml_path.name}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_xml)
    
    return output_path

def reconstruct_json(xml_path: Path, id_jsons_dir: Path, output_dir: Path):
    """Reconstruct JSON files from translated XML and ID mappings."""
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    
    for file_node in root.findall(".//file"):
        # Get the original JSON path and load ID mapping
        relative_path = Path(file_node.get("src"))
        id_json_path = id_jsons_dir / relative_path
        id_data = load_json_file(str(id_json_path))
        
        # Create translation mapping
        translations = {
            int(node.get("id")): node.text
            for node in file_node.findall("s")
        }
        
        # Reconstruct JSON with translations
        output_json = reconstruct_with_translations(id_data, translations)
        
        # Save translated JSON
        output_path = output_dir / relative_path
        save_json_file(output_json, str(output_path))

def reconstruct_with_translations(id_data: Dict[str, Any], translations: Dict[int, str]) -> Dict[str, Any]:
    """Reconstruct JSON structure with translated values."""
    result = {}
    for key, value in id_data.items():
        if isinstance(value, int):
            result[key] = translations.get(value, str(value))
        elif isinstance(value, dict):
            result[key] = reconstruct_with_translations(value, translations)
        else:
            result[key] = value
    return result

def translate_value(value: str, plugin: TranslationPlugin, source_lang: str, target_lang: str) -> str:
    """Translate a single string value using the provided plugin."""
    try:
        return plugin.translate(value, source_lang, target_lang)
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to translate '{value}': {e}[/yellow]")
        return value

@app.command()
def translate(
    source_lang: str = typer.Argument(..., help="Source language code (e.g., 'en')"),
    target_lang: str = typer.Argument(..., help="Target language code (e.g., 'es')"),
    input_dir: str = typer.Option(".", help="Input directory containing JSON files"),
    plugin_name: str = typer.Option("openai", help="Name of the translation plugin to use"),
    debug: bool = typer.Option(False, help="Run in debug mode (preserve intermediate files)"),
):
    """
    Translate all JSON files in a directory from source language to target language.
    """
    # Initialize
    base_dir = Path(input_dir)
    output_dir = Path("output") / target_lang
    tmp_dir = Path("tmp")
    json_files = find_json_files(input_dir)
    
    if not json_files:
        console.print("[red]No JSON files found in the specified directory[/red]")
        raise typer.Exit(1)
    
    # Get the translation plugin
    plugin = PluginRegistry.get_plugin(plugin_name)
    if not plugin:
        console.print(f"[red]Error: Plugin '{plugin_name}' not found[/red]")
        raise typer.Exit(1)
    
    with Progress() as progress:
        # Step 1: Generate XML and ID mappings
        task = progress.add_task("[cyan]Generating XML...", total=1)
        xml_path, _ = generate_xml(json_files, base_dir)
        progress.update(task, completed=1)
        
        # Step 2: Translate XML
        task = progress.add_task("[cyan]Translating...", total=1)
        translated_xml = translate_xml(xml_path, source_lang, target_lang, plugin)
        progress.update(task, completed=1)
        
        # Step 3: Reconstruct JSON files
        task = progress.add_task("[cyan]Reconstructing JSON files...", total=1)
        reconstruct_json(translated_xml, tmp_dir, output_dir)
        progress.update(task, completed=1)
    
    # Clean up temporary files unless in debug mode
    if not debug:
        shutil.rmtree(tmp_dir)
        console.print("[cyan]Cleaned up temporary files[/cyan]")
    else:
        console.print(f"[yellow]Debug mode: Temporary files preserved in {tmp_dir}[/yellow]")
    
    console.print(f"[green]Translation completed! Output saved in: {output_dir}[/green]")

@app.command()
def list_plugins():
    """List all available translation plugins."""
    plugins = PluginRegistry.get_available_plugins()
    if not plugins:
        console.print("[yellow]No plugins found[/yellow]")
        return
    
    console.print("\n[bold]Available Translation Plugins:[/bold]")
    for plugin_name in plugins:
        console.print(f"- {plugin_name}")

@app.command()
def reviewer(
    input_dir: str = typer.Argument(..., help="Input directory containing source language files"),
    output_dir: str = typer.Argument(..., help="Directory containing target language files"),
    app_name: str = typer.Option("translation_reviewer", help="Name for the Sanic application"),
    port: int = typer.Option(8000, help="Port to run the server on")
):
    """
    Launch a web-based reviewer interface for comparing and editing translations.
    """
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    # Create reviewer directory if it doesn't exist
    reviewer_dir = Path("reviewer")
    reviewer_dir.mkdir(exist_ok=True)
    
    # Copy static files from templates
    template_dir = Path("templates/reviewer")
    for template_file in ["reviewer.xhtml", "reviewer.js", "reviewer.css"]:
        shutil.copy(template_dir / template_file, reviewer_dir / template_file)

    # Initialize Sanic app using AppLoader
    from sanic.worker.loader import AppLoader
    from sanic import Sanic
    from lingora.sanic_app import create_app

    # Create app loader with configuration
    config = {
        "input_path": input_path,
        "output_path": output_path,
        "reviewer_dir": reviewer_dir
    }
    
    loader = AppLoader(
        factory=partial(create_app, app_name, config),
        #debug=True
    )
    
    console.print("[green]Starting translation reviewer server...[/green]")
    try:
        app = loader.load()
        app.prepare(port=port, dev=True)
        
        # Open browser after server starts
        app.add_task(partial(webbrowser.open, f'http://localhost:{port}'))
        
        # Start the server
        Sanic.serve(primary=app, app_loader=loader)
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down reviewer server...[/yellow]")
    except Exception as e:
        console.print(f"[red]Error starting server: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 