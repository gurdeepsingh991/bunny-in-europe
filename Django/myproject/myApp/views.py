from django.shortcuts import render
from .models import Travel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from django.conf import settings
import os
from .html_to_docx import convert_html_to_docx


@api_view(['GET', 'POST'])
def create_travel(request):
    if request.method == 'POST':
        Travel.objects.create(
            has_traveled_toeurope=request.data.get("has_traveled_toeurope"),
            contries=request.data.get("countries"),
        )

        return Response({
            "message": "Travel Created",
        })

    if request.method == 'GET':
        travel = Travel.objects.last()

        if not travel:
            return Response({"message": "No data found"})

        return Response({
            "has_traveled_toeurope": travel.has_traveled_toeurope,
            "countries": travel.contries,
        })


@api_view(['GET', 'POST'])
def convert_html_to_word(request):
    """
    API endpoint to convert HTML template to Word document.
    
    GET: Download Word document from template.html
    POST: Convert custom HTML to Word document
    
    GET: http://127.0.0.1:8000/api/convert-html-to-word/
    
    POST body example:
    {
        "html_content": "<p>Your HTML here</p>",
        "filename": "document.docx",
        "config": {
            "fonts": {
                "heading": {"name": "Arial", "sizes": {"h1": 24}, "color": "#0d1831"},
                "default": {"name": "Calibri", "size": 11}
            }
        }
    }
    """
    
    try:
        if request.method == 'POST':
            html_content = request.data.get('html_content')
            filename = request.data.get('filename', 'document.docx')
            config = request.data.get('config')
            
            if not html_content:
                return Response(
                    {"error": "html_content is required"},
                    status=400
                )
            
            docx_buffer = convert_html_to_docx(html_content, config)
            
            response = FileResponse(
                docx_buffer,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                filename=filename
            )
            return response
        
        elif request.method == 'GET':
            template_path = os.path.join(
                settings.BASE_DIR,
                'myApp',
                'template.html'
            )
            
            if not os.path.exists(template_path):
                return Response(
                    {"error": f"Template file not found at {template_path}"},
                    status=404
                )
            
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            config = {
                "fix_html": True,
                "strip_interactive": True,
                "strip_event_handlers": True,
                "normalize_tables": True,
                "decode_html_entities": True,
                "remove_empty_paragraphs": False,
                "remove_empty_spans": False,
                "flatten_nested_spans": False,
                "remove_comments": False,
                "strip_whitespace": False,
                
                "div_mappings": {},
                "class_styles": {},
                "indent_mapping": {},
                "apply_th_styles": True,
                
                "fonts": {
                    "default": {
                        "name": "Verdana",
                        "size": 10,
                        "color": "#222222"
                    },
                    "table": {
                        "name": "Verdana",
                        "size": 9
                    },
                    "heading": {
                        "name": "Verdana",
                        "sizes": {
                            "h1": 22,
                            "h2": 18,
                            "h3": 16
                        },
                        "color": "#0d1831"
                    }
                },
                "class_styles": {
                    "table-dotted": {
                        "border": "1px dotted #999"
                    },
                    "table-dashed": {
                        "border": "1px dashed #666"
                    },
                    "cell-muted": {
                        "background-color": "#f4f4f2"
                    },
                    "cell-strong-border": {
                        "border-left": "2px solid #333"
                    }
                },
                
                
                
                "include_images": True,
                "image_placeholder": True,
                "max_image_width": None,
                
                "table_style": None,
                "flatten_nested_tables": True,
                "table_borders": False,
                "fix_colspan_rowspan": True,
                
                "default_paragraph_style": None,
                "default_alignment": None,
                "convert_br": True,
                
                "span_as_stack": True,
                "apply_span_styles": True,
                "color_map": {},
                
                "allow_existing_document": True,
                "enable_chunk_mode": False,
                "debug": False,
                
                #table borders
                "respect_inline_table_styles": True,
                "respect_inline_cell_styles": True,

                "default_table_border": {
                    "style": "dashed",
                    "size": 4,
                    "color": "auto"
                },

                "default_cell_border": None,
                "default_cell_shading": None,
            }
            
            docx_buffer = convert_html_to_docx(html_content, config)
            
            response = FileResponse(
                docx_buffer,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                filename='works_order_agreement.docx'
            )
            return response
    
    except Exception as e:
        return Response(
            {"error": f"Error converting HTML to Word: {str(e)}"},
            status=500
        )
