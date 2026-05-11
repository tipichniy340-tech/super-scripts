"""
Unit tests for AutoDiag Pro core diagnostic module
"""
import pytest
from unittest.mock import patch, MagicMock
import time

from core.diagnostic import (
    Language,
    VehicleType,
    Manufacturer,
    DiagnosticTroubleCode,
    LiveDataParameter,
    VehicleInfo,
    DiagnosticSession,
)


class TestLanguage:
    """Tests for Language enum."""

    def test_language_values(self):
        """Test language enum values."""
        assert Language.EN.value == "en"
        assert Language.RU.value == "ru"


class TestVehicleType:
    """Tests for VehicleType enum."""

    def test_vehicle_type_values(self):
        """Test vehicle type enum values."""
        assert VehicleType.PASSENGER.value == "passenger"
        assert VehicleType.TRUCK.value == "truck"


class TestManufacturer:
    """Tests for Manufacturer enum."""

    def test_manufacturer_values(self):
        """Test manufacturer enum values."""
        manufacturers = [
            Manufacturer.TOYOTA.value,
            Manufacturer.LEXUS.value,
            Manufacturer.NISSAN.value,
            Manufacturer.MAZDA.value,
            Manufacturer.HONDA.value,
            Manufacturer.GAZ.value,
            Manufacturer.LADA.value,
        ]
        assert len(manufacturers) == 7


class TestDiagnosticTroubleCode:
    """Tests for DiagnosticTroubleCode dataclass."""

    def test_dtc_creation(self):
        """Test DTC creation."""
        dtc = DiagnosticTroubleCode(
            code="P0300",
            description="Random Misfire",
            description_ru="Случайные пропуски",
            severity="high",
            system="Engine"
        )
        assert dtc.code == "P0300"
        assert dtc.severity == "high"
        assert dtc.system == "Engine"


class TestLiveDataParameter:
    """Tests for LiveDataParameter dataclass."""

    def test_live_data_creation(self):
        """Test live data parameter creation."""
        param = LiveDataParameter(
            name="RPM",
            name_ru="Обороты",
            value=750.0,
            unit="rpm",
            min_value=0.0,
            max_value=7000.0,
            status="normal"
        )
        assert param.value == 750.0
        assert param.status == "normal"


class TestVehicleInfo:
    """Tests for VehicleInfo dataclass."""

    def test_vehicle_info_creation(self):
        """Test vehicle info creation."""
        info = VehicleInfo(
            vin="1HGBH41JXMN109186",
            manufacturer="Honda",
            model="Accord",
            year=2021,
            vehicle_type=VehicleType.PASSENGER,
            engine="2.0L I4",
            transmission="CVT"
        )
        assert info.vin == "1HGBH41JXMN109186"
        assert info.year == 2021
        assert info.vehicle_type == VehicleType.PASSENGER


class TestDiagnosticSession:
    """Tests for DiagnosticSession class."""

    def test_session_initialization(self):
        """Test session initialization."""
        session = DiagnosticSession()
        assert session.connected is False
        assert session.language == Language.EN
        assert session.dtcs == []
        assert session.live_data == []

    def test_session_with_language(self):
        """Test session with Russian language."""
        session = DiagnosticSession(language=Language.RU)
        assert session.language == Language.RU

    @patch('core.diagnostic.time.sleep')
    def test_connect(self, mock_sleep):
        """Test vehicle connection."""
        session = DiagnosticSession()
        success = session.connect("COM3", "AUTO")
        
        assert success is True
        assert session.connected is True
        assert session.protocol == "AUTO"
        assert session.vehicle_info is not None

    def test_disconnect(self):
        """Test vehicle disconnection."""
        session = DiagnosticSession()
        session.connected = True
        session.vehicle_info = VehicleInfo(
            vin="TEST", manufacturer="Test", model="Test",
            year=2020, vehicle_type=VehicleType.PASSENGER,
            engine="Test", transmission="Test"
        )
        
        session.disconnect()
        
        assert session.connected is False
        assert session.vehicle_info is None
        assert session.dtcs == []

    @patch('core.diagnostic.time.sleep')
    def test_read_dtcs(self, mock_sleep):
        """Test reading DTCs."""
        session = DiagnosticSession()
        session.connect("COM3")
        
        dtcs = session.read_dtcs()
        
        assert len(dtcs) > 0
        assert isinstance(dtcs[0], DiagnosticTroubleCode)
        assert dtcs[0].code in ["P0300", "P0171"]

    def test_read_dtcs_not_connected(self):
        """Test reading DTCs when not connected."""
        session = DiagnosticSession()
        
        with pytest.raises(ConnectionError):
            session.read_dtcs()

    @patch('core.diagnostic.time.sleep')
    def test_clear_dtcs(self, mock_sleep):
        """Test clearing DTCs."""
        session = DiagnosticSession()
        session.connect("COM3")
        session.read_dtcs()
        
        success = session.clear_dtcs()
        
        assert success is True
        assert session.dtcs == []

    @patch('core.diagnostic.time.sleep')
    def test_read_live_data(self, mock_sleep):
        """Test reading live data."""
        session = DiagnosticSession()
        session.connect("COM3")
        
        data = session.read_live_data()
        
        assert len(data) > 0
        assert isinstance(data[0], LiveDataParameter)
        assert data[0].value >= 0

    def test_read_live_data_not_connected(self):
        """Test reading live data when not connected."""
        session = DiagnosticSession()
        
        with pytest.raises(ConnectionError):
            session.read_live_data()

    @patch('core.diagnostic.time.sleep')
    def test_perform_actuator_test(self, mock_sleep):
        """Test actuator test."""
        session = DiagnosticSession()
        session.connect("COM3")
        
        success = session.perform_actuator_test("Fuel Pump")
        
        assert success is True

    @patch('core.diagnostic.time.sleep')
    def test_encode_module(self, mock_sleep):
        """Test module encoding."""
        session = DiagnosticSession()
        session.connect("COM3")
        
        config = {"option": "test"}
        success = session.encode_module("ECM", config)
        
        assert success is True

    @patch('core.diagnostic.time.sleep')
    @patch('core.diagnostic.os.path.exists')
    def test_flash_ecu(self, mock_exists, mock_sleep):
        """Test ECU flashing."""
        mock_exists.return_value = True
        
        session = DiagnosticSession()
        session.connect("COM3")
        
        success = session.flash_ecu("ECM", "firmware.bin")
        
        assert success is True

    def test_get_supported_manufacturers(self):
        """Test getting supported manufacturers."""
        session = DiagnosticSession()
        manufacturers = session.get_supported_manufacturers()
        
        assert len(manufacturers) == 7
        assert "toyota" in manufacturers
        assert "honda" in manufacturers
        assert "lada" in manufacturers

    def test_get_translation_english(self):
        """Test English translations."""
        session = DiagnosticSession(language=Language.EN)
        
        assert session.get_translation("connecting") == "Connecting to vehicle..."
        assert session.get_translation("connected") == "Connected to vehicle"

    def test_get_translation_russian(self):
        """Test Russian translations."""
        session = DiagnosticSession(language=Language.RU)
        
        assert session.get_translation("connecting") == "Подключение к автомобилю..."
        assert session.get_translation("connected") == "Подключено к автомобилю"

    def test_get_translation_unknown_key(self):
        """Test unknown translation key."""
        session = DiagnosticSession()
        
        result = session.get_translation("unknown_key")
        assert result == "unknown_key"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
