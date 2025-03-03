import argparse
from rich.console import Console
from rich.table import Table
from src.parser import KindleHighlightAnalyzer

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze Kindle highlights and notes')
    parser.add_argument('file', help='Path to your My Clippings.txt file')
    parser.add_argument('--query', '-q', help='Search query to find similar highlights', default=None)
    parser.add_argument('--book', '-b', help='Book title to analyze', default=None)
    parser.add_argument('--connections', '-c', action='store_true', help='Find connections between books')
    parser.add_argument('--export', '-e', choices=['markdown', 'csv', 'json'], help='Export highlights to specified format')
    parser.add_argument('--analytics', '-a', action='store_true', help='Perform analytics on highlights')
    parser.add_argument('--config', '-g', action='store_true', help='Show configuration settings')
    
    
    args = parser.parse_args()
    console = Console()

    try:
        # Initialize analyzer
        with console.status("[bold green]Loading model...") as status:
            analyzer = KindleHighlightAnalyzer()
            
            # Load highlights
            status.update("[bold green]Loading highlights...")
            highlights = analyzer.parse_highlights_file(args.file)
            console.print(f"\n📚 Loaded [bold]{len(highlights)}[/bold] highlights from [bold]{len(set(h.book_title for h in highlights))}[/bold] books\n")
            
            # Compute embeddings
            status.update("[bold green]Computing embeddings...")
            analyzer.compute_embeddings()

        # Search functionality
        if args.query:
            console.print(f"\n🔍 Finding highlights similar to: [bold]'{args.query}'[/bold]\n")
            similar = analyzer.find_similar_highlights(args.query)
            
            table = Table(title="Similar Highlights")
            table.add_column("Similarity", justify="right", style="cyan")
            table.add_column("Book", style="magenta")
            table.add_column("Highlight", style="green")
            
            for similarity, highlight in similar:
                table.add_row(
                    f"{similarity:.3f}",
                    highlight.book_title,
                    highlight.content[:100] + "..." if len(highlight.content) > 100 else highlight.content
                )
            console.print(table)

        # Book insights
        if args.book:
            console.print(f"\n📖 Analyzing book: [bold]'{args.book}'[/bold]\n")
            insights = analyzer.generate_book_insights(args.book)
            
            if insights:
                console.print(f"Total highlights: [bold]{insights['total_highlights']}[/bold]")
                console.print("\nMost representative highlights:")
                
                for similarity, highlight in insights['representative_highlights']:
                    console.print(f"\n[bold cyan]{similarity:.3f}[/bold cyan] - {highlight.content}")
                    
                if insights['temporal_distribution']:
                    console.print("\nReading period:")
                    console.print(f"Started: {insights['temporal_distribution']['first_highlight']:%Y-%m-%d}")
                    console.print(f"Finished: {insights['temporal_distribution']['last_highlight']:%Y-%m-%d}")
                    console.print(f"Days: {insights['temporal_distribution']['total_days']}")
            else:
                console.print("[red]No insights found for this book[/red]")

        # Find connections
        if args.connections:
            console.print("\n🔗 Finding connections between books\n")
            connections = analyzer.find_connections(min_similarity=0.7)
            
            table = Table(title="Connections Between Books")
            table.add_column("Similarity", justify="right", style="cyan")
            table.add_column("Book 1", style="magenta")
            table.add_column("Highlight 1", style="green")
            table.add_column("Book 2", style="magenta")
            table.add_column("Highlight 2", style="green")
            
            for similarity, h1, h2 in connections[:5]:
                table.add_row(
                    f"{similarity:.3f}",
                    h1.book_title,
                    h1.content[:50] + "..." if len(h1.content) > 50 else h1.content,
                    h2.book_title,
                    h2.content[:50] + "..." if len(h2.content) > 50 else h2.content
                )
            console.print(table)

    except FileNotFoundError:
        console.print(f"[red]Error:[/red] Could not find file '{args.file}'")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")

if __name__ == '__main__':
    main()