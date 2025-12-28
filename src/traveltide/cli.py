import typer

app = typer.Typer(help="TravelTide customer segmentation & rewards (golden path entrypoint).")

@app.command()
def demo() -> None:
    """Placeholder command. The golden path will be implemented later."""
    typer.echo("Demo placeholder: pipeline not implemented yet.")

def main() -> None:
    app()

if __name__ == "__main__":
    main()
