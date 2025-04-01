"""
GUID validation rule for FlatForge.

This module contains the GuidRule class that validates GUID/UUID formats.
"""
import uuid
import re
from typing import Dict, List, Optional, Any, Tuple

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class GuidRule(ValidationRule):
    """Rule that validates GUID/UUID formats."""
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a GuidRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params or {})
        self.version = self.params.get("version")
        self.strip_spaces = self.params.get("strip_spaces", True)
        self.strip_hyphens = self.params.get("strip_hyphens", True)
        self.error_message = self.params.get("error_message", "Invalid GUID format")
        
    def _clean_guid(self, value: str) -> str:
        """
        Clean a GUID string by removing spaces, braces, and other formatting.
        
        Args:
            value: The GUID string to clean
            
        Returns:
            str: The cleaned GUID string
        """
        if not value:
            return ""
            
        guid = str(value).strip()
        
        # Remove URN prefix if present
        if guid.startswith("urn:uuid:"):
            guid = guid[9:]
            
        # Remove braces and parentheses
        guid = re.sub(r"[{}\(\)]", "", guid)
        
        # Remove spaces if configured
        if self.strip_spaces:
            guid = guid.replace(" ", "")
            
        # Remove hyphens if configured
        if self.strip_hyphens:
            guid = guid.replace("-", "")
            
        return guid
        
    def validate(self, record: ParsedRecord) -> Tuple[bool, Optional[str]]:
        """
        Validate a GUID/UUID field.
        
        Args:
            record: The record containing the field value
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        try:
            field_value = record.field_values[self.params["field"]]
            cleaned_guid = self._clean_guid(field_value.value)
            
            if not cleaned_guid:
                return False, "Invalid GUID/UUID format"
                
            # Add hyphens back in standard positions if they were removed
            if self.strip_hyphens and len(cleaned_guid) == 32:
                cleaned_guid = f"{cleaned_guid[:8]}-{cleaned_guid[8:12]}-{cleaned_guid[12:16]}-{cleaned_guid[16:20]}-{cleaned_guid[20:]}"
                
            guid = uuid.UUID(cleaned_guid)
            
            if self.version is not None and guid.version != self.version:
                return False, f"Field must be a UUID version {self.version}"
                
            return True, None
                
        except KeyError:
            return False, f"Field {self.params['field']} not found in record"
        except ValueError:
            return False, self.error_message 