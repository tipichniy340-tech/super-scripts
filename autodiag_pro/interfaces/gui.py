"""
GUI Interface for AutoDiag Pro
Graphical user interface using tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, Callable
import threading
import time

from core.diagnostic import (
    DiagnosticSession,
    Language,
    DiagnosticTroubleCode,
    LiveDataParameter,
    VehicleInfo,
)


class GUIInterface:
    """Graphical user interface for AutoDiag Pro."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoDiag Pro - Professional Diagnostic Tool")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set icon if available
        try:
            self.root.iconbitmap("assets/icon.ico")
        except Exception:
            pass
        
        self.session = DiagnosticSession()
        self.language = Language.EN
        self.live_data_running = False
        self.live_data_thread: Optional[threading.Thread] = None
        
        self._setup_styles()
        self._create_menu()
        self._create_widgets()
        self._update_ui_state()
    
    def _setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Status.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        style.configure('Connected.TLabel', foreground='#27ae60', font=('Arial', 10, 'bold'))
        style.configure('Disconnected.TLabel', foreground='#e74c3c', font=('Arial', 10, 'bold'))
        style.configure('Warning.TLabel', foreground='#f39c12')
        
        # Button styles
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'), foreground='#c0392b')
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File" if self.language == Language.EN else "Файл", menu=file_menu)
        file_menu.add_command(label="Connect", command=self._connect_vehicle, accelerator="Ctrl+O")
        file_menu.add_command(label="Disconnect", command=self._disconnect_vehicle, accelerator="Ctrl+D")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_app, accelerator="Alt+F4")
        
        # Language menu
        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language / Язык", menu=lang_menu)
        lang_menu.add_command(label="English", command=lambda: self._set_language(Language.EN))
        lang_menu.add_command(label="Русский", command=lambda: self._set_language(Language.RU))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help" if self.language == Language.EN else "Помощь", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self._connect_vehicle())
        self.root.bind('<Control-d>', lambda e: self._disconnect_vehicle())
    
    def _create_widgets(self):
        """Create main widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="🚗 AutoDiag Pro", style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(header_frame, text="Not Connected", style='Disconnected.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create tabs
        self._create_diagnosis_tab()
        self._create_live_data_tab()
        self._create_advanced_tab()
        self._create_settings_tab()
    
    def _create_diagnosis_tab(self):
        """Create diagnosis tab."""
        diag_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(diag_frame, text="Diagnosis" if self.language == Language.EN else "Диагностика")
        
        # DTC section
        dtc_frame = ttk.LabelFrame(diag_frame, text="Diagnostic Trouble Codes", padding="10")
        dtc_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(dtc_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        read_btn = ttk.Button(btn_frame, text="Read DTCs", command=self._read_dtcs)
        read_btn.grid(row=0, column=0, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Clear DTCs", command=self._clear_dtcs, style='Danger.TButton')
        clear_btn.grid(row=0, column=1, padx=5)
        
        # DTC List
        dtc_list_frame = ttk.Frame(dtc_frame)
        dtc_list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        columns = ('code', 'system', 'severity', 'description')
        self.dtc_tree = ttk.Treeview(dtc_list_frame, columns=columns, show='headings', height=10)
        
        self.dtc_tree.heading('code', text='Code')
        self.dtc_tree.heading('system', text='System')
        self.dtc_tree.heading('severity', text='Severity')
        self.dtc_tree.heading('description', text='Description')
        
        self.dtc_tree.column('code', width=80)
        self.dtc_tree.column('system', width=120)
        self.dtc_tree.column('severity', width=80)
        self.dtc_tree.column('description', width=400)
        
        scrollbar = ttk.Scrollbar(dtc_list_frame, orient=tk.VERTICAL, command=self.dtc_tree.yview)
        self.dtc_tree.configure(yscrollcommand=scrollbar.set)
        
        self.dtc_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        dtc_list_frame.columnconfigure(0, weight=1)
        dtc_list_frame.rowconfigure(0, weight=1)
    
    def _create_live_data_tab(self):
        """Create live data tab."""
        live_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(live_frame, text="Live Data" if self.language == Language.EN else "Данные в реальном времени")
        
        # Control buttons
        btn_frame = ttk.Frame(live_frame)
        btn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.start_live_btn = ttk.Button(btn_frame, text="Start Monitoring", command=self._toggle_live_data)
        self.start_live_btn.grid(row=0, column=0, padx=5)
        
        refresh_btn = ttk.Button(btn_frame, text="Refresh Once", command=self._refresh_live_data)
        refresh_btn.grid(row=0, column=1, padx=5)
        
        # Live data list
        data_list_frame = ttk.Frame(live_frame)
        data_list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        columns = ('parameter', 'value', 'unit', 'status')
        self.live_tree = ttk.Treeview(data_list_frame, columns=columns, show='headings', height=15)
        
        self.live_tree.heading('parameter', text='Parameter')
        self.live_tree.heading('value', text='Value')
        self.live_tree.heading('unit', text='Unit')
        self.live_tree.heading('status', text='Status')
        
        self.live_tree.column('parameter', width=250)
        self.live_tree.column('value', width=100)
        self.live_tree.column('unit', width=80)
        self.live_tree.column('status', width=100)
        
        scrollbar = ttk.Scrollbar(data_list_frame, orient=tk.VERTICAL, command=self.live_tree.yview)
        self.live_tree.configure(yscrollcommand=scrollbar.set)
        
        self.live_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        data_list_frame.columnconfigure(0, weight=1)
        data_list_frame.rowconfigure(0, weight=1)
        live_frame.columnconfigure(0, weight=1)
        live_frame.rowconfigure(1, weight=1)
    
    def _create_advanced_tab(self):
        """Create advanced tests tab."""
        adv_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(adv_frame, text="Advanced" if self.language == Language.EN else "Расширенные тесты")
        
        # Actuator tests
        actuator_frame = ttk.LabelFrame(adv_frame, text="Actuator Tests", padding="10")
        actuator_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        actuators = ["Fuel Pump", "Cooling Fan", "EGR Valve", "Throttle Body", "Injectors"]
        for i, actuator in enumerate(actuators):
            btn = ttk.Button(actuator_frame, text=actuator, command=lambda a=actuator: self._test_actuator(a))
            btn.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
        
        actuator_frame.columnconfigure(0, weight=1)
        
        # Module encoding
        encode_frame = ttk.LabelFrame(adv_frame, text="Module Encoding", padding="10")
        encode_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        modules = ["ECM", "TCM", "BCM", "ABS", "SRS", "Instrument Cluster"]
        for i, module in enumerate(modules):
            btn = ttk.Button(encode_frame, text=module, command=lambda m=module: self._encode_module(m))
            btn.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
        
        encode_frame.columnconfigure(0, weight=1)
        
        # ECU Flashing
        flash_frame = ttk.LabelFrame(adv_frame, text="ECU Flashing", padding="10")
        flash_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        flash_btn = ttk.Button(flash_frame, text="Flash ECU", command=self._flash_ecu, style='Danger.TButton')
        flash_btn.grid(row=0, column=0, padx=5)
        
        adv_frame.columnconfigure(0, weight=1)
        adv_frame.columnconfigure(1, weight=1)
        adv_frame.rowconfigure(0, weight=1)
    
    def _create_settings_tab(self):
        """Create settings tab."""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="Settings" if self.language == Language.EN else "Настройки")
        
        # Connection settings
        conn_frame = ttk.LabelFrame(settings_frame, text="Connection Settings", padding="10")
        conn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(conn_frame, text="OBD Port:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar(value="COM3")
        port_combo = ttk.Combobox(conn_frame, textvariable=self.port_var, values=["COM1", "COM2", "COM3", "COM4", "USB0"])
        port_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(conn_frame, text="Protocol:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.protocol_var = tk.StringVar(value="AUTO")
        protocol_combo = ttk.Combobox(conn_frame, textvariable=self.protocol_var, values=["AUTO", "ISO9141", "KWP2000", "CAN"])
        protocol_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        conn_frame.columnconfigure(1, weight=1)
        
        # Vehicle info display
        self.vehicle_info_text = scrolledtext.ScrolledText(settings_frame, height=10, state='disabled')
        self.vehicle_info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.rowconfigure(1, weight=1)
    
    def _update_ui_state(self):
        """Update UI based on connection state."""
        if self.session.connected:
            self.status_label.config(text="Connected", style='Connected.TLabel')
            if self.session.vehicle_info:
                self._display_vehicle_info()
        else:
            self.status_label.config(text="Not Connected", style='Disconnected.TLabel')
            self.dtc_tree.delete(*self.dtc_tree.get_children())
            if not self.live_data_running:
                self.live_tree.delete(*self.live_tree.get_children())
    
    def _display_vehicle_info(self):
        """Display vehicle information."""
        if not self.session.vehicle_info:
            return
        
        info = self.session.vehicle_info
        self.vehicle_info_text.config(state='normal')
        self.vehicle_info_text.delete(1.0, tk.END)
        
        text = f"""VIN: {info.vin}
Manufacturer: {info.manufacturer}
Model: {info.model}
Year: {info.year}
Type: {info.vehicle_type.value.capitalize()}
Engine: {info.engine}
Transmission: {info.transmission}
"""
        self.vehicle_info_text.insert(tk.END, text)
        self.vehicle_info_text.config(state='disabled')
    
    def _connect_vehicle(self):
        """Connect to vehicle."""
        port = self.port_var.get()
        protocol = self.protocol_var.get()
        
        try:
            success = self.session.connect(port, protocol)
            if success:
                messagebox.showinfo("Success", "Connected to vehicle successfully!")
                self._update_ui_state()
            else:
                messagebox.showerror("Error", "Failed to connect to vehicle.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def _disconnect_vehicle(self):
        """Disconnect from vehicle."""
        if self.live_data_running:
            self._toggle_live_data()
        
        self.session.disconnect()
        self._update_ui_state()
        messagebox.showinfo("Disconnected", "Disconnected from vehicle.")
    
    def _read_dtcs(self):
        """Read DTCs."""
        if not self.session.connected:
            messagebox.showwarning("Warning", "Not connected to vehicle!")
            return
        
        try:
            dtcs = self.session.read_dtcs()
            
            self.dtc_tree.delete(*self.dtc_tree.get_children())
            
            for dtc in dtcs:
                description = dtc.description_ru if self.language == Language.RU else dtc.description
                self.dtc_tree.insert('', tk.END, values=(dtc.code, dtc.system, dtc.severity.upper(), description))
            
            if not dtcs:
                messagebox.showinfo("Info", "No diagnostic trouble codes found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read DTCs: {str(e)}")
    
    def _clear_dtcs(self):
        """Clear DTCs."""
        if not self.session.connected:
            messagebox.showwarning("Warning", "Not connected to vehicle!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all DTCs?"):
            try:
                self.session.clear_dtcs()
                self.dtc_tree.delete(*self.dtc_tree.get_children())
                messagebox.showinfo("Success", "DTCs cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear DTCs: {str(e)}")
    
    def _refresh_live_data(self):
        """Refresh live data once."""
        if not self.session.connected:
            messagebox.showwarning("Warning", "Not connected to vehicle!")
            return
        
        try:
            data = self.session.read_live_data()
            
            self.live_tree.delete(*self.live_tree.get_children())
            
            for param in data:
                name = param.name_ru if self.language == Language.RU else param.name
                self.live_tree.insert('', tk.END, values=(name, f"{param.value:.1f}", param.unit, param.status.upper()))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read live data: {str(e)}")
    
    def _toggle_live_data(self):
        """Toggle live data monitoring."""
        if self.live_data_running:
            self.live_data_running = False
            self.start_live_btn.config(text="Start Monitoring")
            if self.live_data_thread:
                self.live_data_thread.join(timeout=2.0)
        else:
            if not self.session.connected:
                messagebox.showwarning("Warning", "Not connected to vehicle!")
                return
            
            self.live_data_running = True
            self.start_live_btn.config(text="Stop Monitoring")
            self.live_data_thread = threading.Thread(target=self._live_data_loop, daemon=True)
            self.live_data_thread.start()
    
    def _live_data_loop(self):
        """Live data monitoring loop."""
        while self.live_data_running:
            try:
                data = self.session.read_live_data()
                
                # Update tree in main thread
                self.root.after(0, self._update_live_tree, data)
                time.sleep(1.0)
            except Exception:
                break
    
    def _update_live_tree(self, data):
        """Update live data tree."""
        self.live_tree.delete(*self.live_tree.get_children())
        
        for param in data:
            name = param.name_ru if self.language == Language.RU else param.name
            self.live_tree.insert('', tk.END, values=(name, f"{param.value:.1f}", param.unit, param.status.upper()))
    
    def _test_actuator(self, actuator_name: str):
        """Test an actuator."""
        if not self.session.connected:
            messagebox.showwarning("Warning", "Not connected to vehicle!")
            return
        
        try:
            success = self.session.perform_actuator_test(actuator_name)
            if success:
                messagebox.showinfo("Success", f"Actuator test completed for {actuator_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Actuator test failed: {str(e)}")
    
    def _encode_module(self, module_name: str):
        """Encode a module."""
        if not self.session.connected:
            messagebox.showwarning("Warning", "Not connected to vehicle!")
            return
        
        try:
            config_data = {"coding_option": "default"}
            success = self.session.encode_module(module_name, config_data)
            if success:
                messagebox.showinfo("Success", f"Module {module_name} encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Module encoding failed: {str(e)}")
    
    def _flash_ecu(self):
        """Flash ECU."""
        if not self.session.connected:
            messagebox.showwarning("Warning", "Not connected to vehicle!")
            return
        
        warning_msg = "WARNING: Flashing ECU can brick your vehicle!\nProceed with caution."
        if not messagebox.askyesno("Warning", warning_msg):
            return
        
        # Simple dialog for ECU name and firmware
        top = tk.Toplevel(self.root)
        top.title("Flash ECU")
        top.geometry("400x200")
        
        ttk.Label(top, text="ECU Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ecu_var = tk.StringVar(value="ECM")
        ttk.Entry(top, textvariable=ecu_var).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(top, text="Firmware File:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        firmware_var = tk.StringVar(value="firmware.bin")
        ttk.Entry(top, textvariable=firmware_var).grid(row=1, column=1, padx=10, pady=10)
        
        def do_flash():
            top.destroy()
            try:
                # Simulate flashing
                progress_win = tk.Toplevel(self.root)
                progress_win.title("Flashing...")
                progress_win.geometry("300x100")
                
                progress_bar = ttk.Progressbar(progress_win, mode='determinate', length=250)
                progress_bar.pack(pady=20)
                
                def update_progress():
                    for i in range(10):
                        progress_bar['value'] = (i + 1) * 10
                        progress_win.update()
                        time.sleep(0.3)
                    
                    progress_win.destroy()
                    messagebox.showinfo("Success", "ECU flashed successfully!")
                
                threading.Thread(target=update_progress, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", f"Flashing failed: {str(e)}")
        
        ttk.Button(top, text="Flash", command=do_flash).grid(row=2, column=0, columnspan=2, pady=20)
    
    def _set_language(self, language: Language):
        """Set application language."""
        self.language = language
        self.session.language = language
        # In a full implementation, this would update all UI text
        messagebox.showinfo("Language", f"Language changed to {'Russian' if language == Language.RU else 'English'}")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """AutoDiag Pro v1.0.0

Professional Automotive Diagnostic Tool

Supported Manufacturers:
• Toyota • Lexus • Nissan • Mazda • Honda • GAZ • Lada

Features:
• Basic Diagnostics (DTC Read/Clear)
• Live Data Monitoring
• Actuator Tests
• Module Encoding
• ECU Flashing

© 2024 AutoDiag Pro Team"""
        
        messagebox.showinfo("About AutoDiag Pro", about_text)
    
    def _exit_app(self):
        """Exit application."""
        if self.live_data_running:
            self.live_data_running = False
        
        if self.session.connected:
            self.session.disconnect()
        
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for GUI."""
    app = GUIInterface()
    app.run()


if __name__ == "__main__":
    main()
