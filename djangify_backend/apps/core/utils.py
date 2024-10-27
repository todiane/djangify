import re
from xml.etree import ElementTree
from django.core.exceptions import ValidationError

def sanitize_svg(svg_content):
    """
    Sanitize SVG content to prevent XSS attacks.
    """
    # List of allowed SVG tags
    ALLOWED_TAGS = {
        'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon',
        'text', 'g', 'defs', 'title', 'desc', 'style'
    }
    
    # List of allowed attributes
    ALLOWED_ATTRIBUTES = {
        'viewbox', 'width', 'height', 'xmlns', 'version', 'baseprofile',
        'x', 'y', 'x1', 'y1', 'x2', 'y2', 'r', 'd', 'transform',
        'style', 'fill', 'stroke', 'stroke-width', 'class', 'id'
    }
    
    try:
        tree = ElementTree.fromstring(svg_content)
        
        # Check for potentially malicious content
        for elem in tree.iter():
            # Remove script elements and event handlers
            if (elem.tag.lower() == 'script' or 
                any(attr.lower().startswith('on') for attr in elem.attrib.keys())):
                raise ValidationError("SVG contains potentially malicious content")
            
            # Remove any non-allowed tags
            if elem.tag.split('}')[-1].lower() not in ALLOWED_TAGS:
                raise ValidationError(f"SVG contains non-allowed tag: {elem.tag}")
            
            # Remove any non-allowed attributes
            allowed_attrs = elem.attrib.copy()
            for attr in elem.attrib:
                if attr.split('}')[-1].lower() not in ALLOWED_ATTRIBUTES:
                    del allowed_attrs[attr]
            elem.attrib = allowed_attrs
            
        # Check for potentially malicious content in style attributes
        for elem in tree.iter():
            style = elem.get('style', '')
            if style and ('javascript:' in style or 'expression(' in style):
                raise ValidationError("SVG contains potentially malicious style content")
        
        return ElementTree.tostring(tree, encoding='unicode')
    
    except ElementTree.ParseError:
        raise ValidationError("Invalid SVG content")

def validate_svg_file(file):
    """
    Validate and sanitize an uploaded SVG file.
    """
    try:
        content = file.read().decode('utf-8')
        sanitized_content = sanitize_svg(content)
        return sanitized_content
    except (UnicodeDecodeError, ValidationError) as e:
        raise ValidationError(f"Invalid SVG file: {str(e)}")
    finally:
        file.seek(0)  # Reset file pointer
        