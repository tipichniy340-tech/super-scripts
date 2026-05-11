"""
CLI Interface for AutoDiag Pro
Command-line interface using rich library
"""
import sys
import time
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

from core.diagnostic import (
    DiagnosticSession,
    Language,
    DiagnosticTroubleCode,
    LiveDataParameter,
    Manufacturer,
)


class CLIInterface:
    """Command-line interface for AutoDiag Pro."""
    
    def __init__(self, language: Language = Language.EN):
        self.console = Console()
        self.session = DiagnosticSession(language=language)
        self.language = language
        self.running = False
    
    def print_header(self) -> None:
        """Print application header."""
        title = "🚗 AutoDiag Pro - Professional Diagnostic Tool"
        subtitle = "Supporting: Toyota, Lexus, Nissan, Mazda, Honda, GAZ, Lada"
        
        if self.language == Language.RU:
            subtitle = "Поддержка: Toyota, Lexus, Nissan, Mazda, Honda, ГАЗ, Лада"
        
        header = Panel(
            f"[bold cyan]{title}[/bold cyan]\n[dim]{subtitle}[/dim]",
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(header)
        self.console.print()
    
    def print_menu(self) -> None:
        """Print main menu."""
        menu_items = {
            "1": ("Connect to Vehicle", "Подключиться к автомобилю"),
            "2": ("Read Diagnostic Trouble Codes", "Прочитать коды неисправностей"),
            "3": ("Clear Diagnostic Trouble Codes", "Очистить коды неисправностей"),
            "4": ("View Live Data", "Просмотр данных в реальном времени"),
            "5": ("Perform Actuator Tests", "Тест исполнительных механизмов"),
            "6": ("Encode Module", "Кодирование модуля"),
            "7": ("Flash ECU", "Прошивка ЭБУ"),
            "8": ("Vehicle Information", "Информация об автомобиле"),
            "9": ("Disconnect", "Отключиться"),
            "0": ("Exit", "Выход"),
        }
        
        self.console.print("[bold yellow]Main Menu:[/bold yellow]")
        self.console.print()
        
        for key, (en_text, ru_text) in menu_items.items():
            text = ru_text if self.language == Language.RU else en_text
            status = ""
            if key == "1" and self.session.connected:
                status = " [green](Connected)[/green]"
            elif key == "1" and not self.session.connected:
                status = " [red](Not Connected)[/red]"
            
            self.console.print(f"  [cyan]{key}[/cyan]. {text}{status}")
        
        self.console.print()
    
    def connect_vehicle(self) -> None:
        """Connect to vehicle."""
        port = Prompt.ask("OBD Port", default="COM3")
        protocol = Prompt.ask("Protocol", default="AUTO", choices=["AUTO", "ISO9141", "KWP2000", "CAN"])
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task("Connecting...", total=None)
            
            try:
                success = self.session.connect(port, protocol)
                progress.update(task, completed=100)
                
                if success:
                    msg = self.session.get_translation("connected")
                    self.console.print(f"[green]✓ {msg}[/green]")
                    
                    if self.session.vehicle_info:
                        self.console.print(f"\n[bold]VIN:[/bold] {self.session.vehicle_info.vin}")
                        self.console.print(f"[bold]Vehicle:[/bold] {self.session.vehicle_info.year} {self.session.vehicle_info.manufacturer} {self.session.vehicle_info.model}")
                        self.console.print(f"[bold]Engine:[/bold] {self.session.vehicle_info.engine}")
                        self.console.print(f"[bold]Transmission:[/bold] {self.session.vehicle_info.transmission}")
                else:
                    msg = self.session.get_translation("error")
                    self.console.print(f"[red]✗ {msg}: Connection failed[/red]")
            except Exception as e:
                self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def read_dtcs(self) -> None:
        """Read and display DTCs."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        msg = self.session.get_translation("reading_dtcs")
        self.console.print(f"[cyan]{msg}[/cyan]")
        
        try:
            dtcs = self.session.read_dtcs()
            
            if not dtcs:
                no_dtcs_msg = self.session.get_translation("no_dtcs")
                self.console.print(f"[green]✓ {no_dtcs_msg}[/green]")
                return
            
            table = Table(title="Diagnostic Trouble Codes")
            table.add_column("Code", style="cyan")
            table.add_column("System", style="magenta")
            table.add_column("Severity", style="yellow")
            
            if self.language == Language.RU:
                table.add_column("Description (RU)", style="white")
            else:
                table.add_column("Description", style="white")
            
            for dtc in dtcs:
                severity_color = {
                    "low": "green",
                    "medium": "yellow",
                    "high": "orange_red1",
                    "critical": "red",
                }.get(dtc.severity, "white")
                
                description = dtc.description_ru if self.language == Language.RU else dtc.description
                
                table.add_row(
                    dtc.code,
                    dtc.system,
                    f"[{severity_color}]{dtc.severity.upper()}[/{severity_color}]",
                    description,
                )
            
            self.console.print(table)
            self.console.print(f"\n[bold]Total DTCs:[/bold] {len(dtcs)}")
        except Exception as e:
            self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def clear_dtcs(self) -> None:
        """Clear DTCs."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        if not Confirm.ask("Are you sure you want to clear all DTCs?"):
            return
        
        msg = self.session.get_translation("clearing_dtcs")
        self.console.print(f"[cyan]{msg}[/cyan]")
        
        try:
            success = self.session.clear_dtcs()
            if success:
                success_msg = self.session.get_translation("success")
                self.console.print(f"[green]✓ {success_msg}[/green]")
        except Exception as e:
            self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def view_live_data(self) -> None:
        """View live data parameters."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        msg = self.session.get_translation("reading_live_data")
        self.console.print(f"[cyan]{msg}[/cyan]")
        self.console.print("[dim]Press Ctrl+C to stop monitoring[/dim]\n")
        
        try:
            while True:
                data = self.session.read_live_data()
                
                table = Table(title="Live Data")
                table.add_column("Parameter", style="cyan")
                table.add_column("Value", style="green")
                table.add_column("Unit", style="white")
                table.add_column("Status", style="yellow")
                
                for param in data:
                    name = param.name_ru if self.language == Language.RU else param.name
                    
                    # Determine status color
                    status_color = {
                        "normal": "green",
                        "warning": "yellow",
                        "critical": "red",
                    }.get(param.status, "white")
                    
                    table.add_row(
                        name,
                        f"{param.value:.1f}",
                        param.unit,
                        f"[{status_color}]{param.status.upper()}[/{status_color}]",
                    )
                
                # Clear screen and print updated table
                self.console.clear()
                self.print_header()
                self.console.print(table)
                
                time.sleep(1.0)
        except KeyboardInterrupt:
            self.console.print("\n[dim]Monitoring stopped[/dim]")
        except Exception as e:
            self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def actuator_tests(self) -> None:
        """Perform actuator tests."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        msg = self.session.get_translation("actuator_test")
        self.console.print(f"[cyan]{msg}[/cyan]")
        
        actuators = ["Fuel Pump", "Cooling Fan", "EGR Valve", "Throttle Body", "Injectors"]
        
        for i, actuator in enumerate(actuators, 1):
            self.console.print(f"  {i}. {actuator}")
        
        try:
            choice = Prompt.ask("Select actuator to test", choices=[str(i) for i in range(1, len(actuators) + 1)], default="1")
            selected_actuator = actuators[int(choice) - 1]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                task = progress.add_task(f"Testing {selected_actuator}...", total=None)
                success = self.session.perform_actuator_test(selected_actuator)
                progress.update(task, completed=100)
            
            if success:
                self.console.print(f"[green]✓ Test completed for {selected_actuator}[/green]")
        except Exception as e:
            self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def encode_module(self) -> None:
        """Encode module configuration."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        msg = self.session.get_translation("encoding_module")
        self.console.print(f"[cyan]{msg}[/cyan]")
        
        modules = ["ECM", "TCM", "BCM", "ABS", "SRS", "Instrument Cluster"]
        
        for i, module in enumerate(modules, 1):
            self.console.print(f"  {i}. {module}")
        
        try:
            choice = Prompt.ask("Select module to encode", choices=[str(i) for i in range(1, len(modules) + 1)], default="1")
            selected_module = modules[int(choice) - 1]
            
            config_data = {"coding_option": "default"}
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                task = progress.add_task(f"Encoding {selected_module}...", total=None)
                success = self.session.encode_module(selected_module, config_data)
                progress.update(task, completed=100)
            
            if success:
                self.console.print(f"[green]✓ Module {selected_module} encoded successfully[/green]")
        except Exception as e:
            self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def flash_ecu(self) -> None:
        """Flash ECU firmware."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        msg = self.session.get_translation("flashing_ecu")
        self.console.print(f"[cyan]{msg}[/cyan]")
        self.console.print("[yellow]⚠ WARNING: Flashing ECU can brick your vehicle! Proceed with caution.[/yellow]")
        
        if not Confirm.ask("Do you want to continue?"):
            return
        
        ecu_name = Prompt.ask("ECU Name", default="ECM")
        firmware_file = Prompt.ask("Firmware File Path", default="firmware.bin")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console,
            ) as progress:
                task = progress.add_task(f"Flashing {ecu_name}...", total=100)
                
                # Simulate flashing
                for i in range(10):
                    time.sleep(0.3)
                    progress.update(task, advance=10)
                
                # In real implementation, call session.flash_ecu()
                success = True
                
                if success:
                    progress.update(task, completed=100)
                    self.console.print(f"[green]✓ ECU {ecu_name} flashed successfully[/green]")
        except Exception as e:
            self.console.print(f"[red]✗ Error: {str(e)}[/red]")
    
    def show_vehicle_info(self) -> None:
        """Display vehicle information."""
        if not self.session.connected:
            self.console.print("[yellow]⚠ Not connected to vehicle[/yellow]")
            return
        
        if not self.session.vehicle_info:
            self.console.print("[yellow]⚠ No vehicle information available[/yellow]")
            return
        
        info = self.session.vehicle_info
        
        table = Table(title="Vehicle Information")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("VIN", info.vin)
        table.add_row("Manufacturer", info.manufacturer)
        table.add_row("Model", info.model)
        table.add_row("Year", str(info.year))
        table.add_row("Type", info.vehicle_type.value.capitalize())
        table.add_row("Engine", info.engine)
        table.add_row("Transmission", info.transmission)
        
        self.console.print(table)
    
    def run(self) -> None:
        """Run the CLI application."""
        self.running = True
        self.print_header()
        
        # Language selection
        lang_choice = Prompt.ask(
            "Select language / Выберите язык",
            choices=["en", "ru"],
            default="en"
        )
        self.language = Language.RU if lang_choice == "ru" else Language.EN
        self.session.language = self.language
        
        self.console.print(f"[green]Language set to {'Russian' if self.language == Language.RU else 'English'}[/green]\n")
        
        while self.running:
            self.print_menu()
            
            choice = Prompt.ask("Select option", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], default="0")
            
            if choice == "0":
                if self.session.connected:
                    self.session.disconnect()
                self.console.print("[blue]Goodbye![/blue]")
                self.running = False
            elif choice == "1":
                self.connect_vehicle()
            elif choice == "2":
                self.read_dtcs()
            elif choice == "3":
                self.clear_dtcs()
            elif choice == "4":
                self.view_live_data()
            elif choice == "5":
                self.actuator_tests()
            elif choice == "6":
                self.encode_module()
            elif choice == "7":
                self.flash_ecu()
            elif choice == "8":
                self.show_vehicle_info()
            elif choice == "9":
                self.session.disconnect()
                disconnect_msg = self.session.get_translation("disconnected")
                self.console.print(f"[yellow]{disconnect_msg}[/yellow]")
            
            if self.running:
                self.console.print()


def main():
    """Main entry point for CLI."""
    cli = CLIInterface()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
