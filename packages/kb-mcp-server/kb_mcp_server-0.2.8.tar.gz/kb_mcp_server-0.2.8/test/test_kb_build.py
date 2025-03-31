#!/usr/bin/env python3
"""
Test script to verify how the knowledge base is saved when not using the --export option.
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to the path so we can import kb_builder
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kb_builder.cli import build_command, setup_logging, create_application

def main():
    """
    Main function to test the build command.
    """
    # Set up logging
    setup_logging(debug=True)
    
    # Method 1: Using build_command
    print("Method 1: Using build_command")
    test_build_command()
    
    # Method 2: Using Application directly
    print("\nMethod 2: Using Application directly")
    test_application_direct()

def test_build_command():
    """
    Test using the build_command function.
    """
    # Create a mock args object
    class Args:
        def __init__(self):
            self.input = [
                "/tmp/finclip-agent-starterkit/contents/data_science.md",
                "/tmp/finclip-agent-starterkit/contents/machine_learning.md",
                "/tmp/finclip-agent-starterkit/contents/neural_networks.md",
                "/tmp/finclip-agent-starterkit/contents/nlp_lm.md"
            ]
            self.json_input = None
            self.extensions = None
            self.config = str(Path(__file__).parent / "knowledgebase" / "kb.yml")
            self.export = None
            self.update = False
            self.debug = True
    
    args = Args()
    
    # Print the configuration
    print(f"Building knowledge base with the following configuration:")
    print(f"  Input files: {args.input}")
    print(f"  Config file: {args.config}")
    print(f"  Export path: {args.export}")
    print(f"  Update mode: {args.update}")
    
    # Run the build command
    build_command(args)
    
    # Check if the knowledge base was created
    check_kb_path()

def test_application_direct():
    """
    Test using the Application class directly.
    """
    config_path = str(Path(__file__).parent / "knowledgebase" / "kb.yml")
    print(f"Creating application with config: {config_path}")
    
    # Create application
    app = create_application(config_path)
    
    # Process documents
    input_files = [
        "/tmp/finclip-agent-starterkit/contents/data_science.md",
        "/tmp/finclip-agent-starterkit/contents/machine_learning.md",
        "/tmp/finclip-agent-starterkit/contents/neural_networks.md",
        "/tmp/finclip-agent-starterkit/contents/nlp_lm.md"
    ]
    
    documents = []
    for file_path in input_files:
        print(f"Processing file: {file_path}")
        try:
            # Extract text using textractor pipeline
            segments = app.pipelines["textractor"](file_path)
            
            # Create documents with metadata
            for i, text in enumerate(segments):
                doc_id = f"{Path(file_path).stem}_{i}"
                documents.append({
                    "id": doc_id,
                    "text": text,
                    "metadata": {
                        "source": file_path,
                        "index": i,
                        "total": len(segments)
                    }
                })
            print(f"Extracted {len(segments)} segments from {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    print(f"Processed {len(documents)} documents")
    
    # Index documents
    print("Indexing documents...")
    app.index()
    
    # Explicitly save the index
    save_path = ".txtai/kb-test"
    print(f"Explicitly saving index to {save_path}")
    os.makedirs(save_path, exist_ok=True)
    app.embeddings.save(save_path)
    
    # Check if the knowledge base was created
    check_kb_path()

def check_kb_path():
    """
    Check if the knowledge base was created and print its contents.
    """
    kb_path = Path(".txtai/kb-test")
    if kb_path.exists():
        print(f"\nKnowledge base was successfully created at: {kb_path.absolute()}")
        print("\nContents of the knowledge base directory:")
        for item in kb_path.glob("**/*"):
            if item.is_file():
                print(f"  {item.relative_to(kb_path)} ({item.stat().st_size} bytes)")
    else:
        print(f"\nError: Knowledge base was not created at the expected location: {kb_path.absolute()}")
        
        # Check if it was created somewhere else
        print("\nSearching for possible knowledge base locations...")
        for path in [Path("."), Path(".txtai")]:
            if path.exists():
                print(f"Contents of {path.absolute()}:")
                for item in path.glob("*"):
                    print(f"  {item.name}")

if __name__ == "__main__":
    main()
