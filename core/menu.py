import click
from core.runner import Runner

def main_menu(runner: Runner) -> None:
    """Display the main menu and handle user input."""
    while True:
        click.echo("""
[ Oblivion Menu ]

1) Web Pentest / Information Gathering
2) Web Application Attack
3) Generator
99) Exit
        """)
        try:
            choice = click.prompt("Oblivion", type=int)
            if choice == 1:
                runner.web_pentest_menu()
            elif choice == 2:
                runner.web_attack_menu()
            elif choice == 3:
                runner.generator_menu()
            elif choice == 99:
                click.echo("Exiting Oblivion")
                break
            else:
                click.echo("Invalid choice. Please select a valid option.")
        except click.Abort:
            click.echo("User interrupted. Exiting.")
            break
        except ValueError:
            click.echo("Please enter a valid number.")
        except Exception as e:
            click.echo(f"Error: {e}")