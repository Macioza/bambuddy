"""
Integration tests for the automatic plate clearing feature.
"""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from backend.app.models.printer import Printer

class TestAutoClearPlateLogic:
    """Test automatic plate clearing logic in on_print_complete."""

    @pytest.mark.asyncio
    async def test_auto_clear_plate_enabled(self):
        """Verify plate is automatically cleared when setting is enabled."""
        printer_id = 1
        with (
            patch("backend.app.main.async_session") as mock_session_maker,
            patch("backend.app.main.printer_manager") as mock_printer_manager,
            patch("backend.app.main.notification_service"),
            patch("backend.app.main.smart_plug_manager"),
            patch("backend.app.main.ws_manager"),
            patch("backend.app.main.ArchiveService"),
        ):
            # Mock the printer object
            mock_printer = MagicMock(spec=Printer)
            mock_printer.id = printer_id
            mock_printer.auto_clear_plate = True
            
            # Mock the database session
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            
            # Mock session.get to return our printer
            mock_session.get = AsyncMock(return_value=mock_printer)
            mock_session_maker.return_value = mock_session

            from backend.app.main import on_print_complete

            await on_print_complete(
                printer_id,
                {
                    "status": "completed",
                    "filename": "/data/Metadata/test.gcode",
                    "subtask_name": "Test",
                    "timelapse_was_active": False,
                },
            )

            # Verify printer_manager.set_plate_cleared was called
            mock_printer_manager.set_plate_cleared.assert_called_once_with(printer_id)

    @pytest.mark.asyncio
    async def test_auto_clear_plate_disabled(self):
        """Verify plate is NOT automatically cleared when setting is disabled."""
        printer_id = 2
        with (
            patch("backend.app.main.async_session") as mock_session_maker,
            patch("backend.app.main.printer_manager") as mock_printer_manager,
            patch("backend.app.main.notification_service"),
            patch("backend.app.main.smart_plug_manager"),
            patch("backend.app.main.ws_manager"),
            patch("backend.app.main.ArchiveService"),
        ):
            # Mock the printer object
            mock_printer = MagicMock(spec=Printer)
            mock_printer.id = printer_id
            mock_printer.auto_clear_plate = False
            
            # Mock the database session
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            
            # Mock session.get to return our printer
            mock_session.get = AsyncMock(return_value=mock_printer)
            mock_session_maker.return_value = mock_session

            from backend.app.main import on_print_complete

            await on_print_complete(
                printer_id,
                {
                    "status": "completed",
                    "filename": "/data/Metadata/test.gcode",
                    "subtask_name": "Test",
                    "timelapse_was_active": False,
                },
            )

            # Verify printer_manager.set_plate_cleared was NOT called
            mock_printer_manager.set_plate_cleared.assert_not_called()
