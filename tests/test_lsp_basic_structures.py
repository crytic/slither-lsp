import json
from slither_lsp.types.lsp_basic_structures import ClientServerInfo, WorkspaceFolder, Position, Range, Location, \
    LocationLink, DiagnosticRelatedInformation, DiagnosticSeverity, DiagnosticTag, Diagnostic, CodeDescription, \
    Command, TextEdit, AnnotatedTextEdit, ChangeAnnotation


def test_client_server_info():
    # Create our expected variables we'll construct tests with.
    expected_name = "test_client_name"
    expected_version = "1.2.3"

    # Test parsing with just a name
    info: ClientServerInfo = ClientServerInfo.from_dict({'name': expected_name})
    assert info.name == expected_name and info.version is None

    # Test round trip conversion
    info_copy = ClientServerInfo.from_dict(info.to_dict())
    assert info == info_copy
    assert json.dumps(info.to_dict()) == json.dumps(info_copy.to_dict())

    # Test parsing with a name and version
    info: ClientServerInfo = ClientServerInfo.from_dict({'name': expected_name, 'version': expected_version})
    assert info.name == expected_name and info.version == expected_version

    # Test round trip conversion
    info_copy = ClientServerInfo.from_dict(info.to_dict())
    assert info == info_copy
    assert json.dumps(info.to_dict()) == json.dumps(info_copy.to_dict())


def test_workspace_folder():
    # Create our expected variables we'll construct tests with.
    workspace_uri = "/test/directory/OK"
    workspace_name = "OK"

    # Test parsing workspace folder with just a uri
    workspace_folder: WorkspaceFolder = WorkspaceFolder.from_dict({'uri': workspace_uri})
    assert workspace_folder.uri == workspace_uri

    # Test round trip conversion of a workspace folder with just a uri
    workspace_folder_copy = WorkspaceFolder.from_dict(workspace_folder.to_dict())
    assert workspace_folder == workspace_folder_copy
    assert json.dumps(workspace_folder.to_dict()) == json.dumps(workspace_folder_copy.to_dict())

    # Test parsing workspace folder with just a uri and name
    workspace_folder: WorkspaceFolder = WorkspaceFolder.from_dict({'uri': workspace_uri, 'name': workspace_name})
    assert workspace_folder.uri == workspace_uri and workspace_folder.name == workspace_name

    # Test round trip conversion of a workspace folder with uri and name
    workspace_folder_copy = WorkspaceFolder.from_dict(workspace_folder.to_dict())
    assert workspace_folder == workspace_folder_copy
    assert json.dumps(workspace_folder.to_dict()) == json.dumps(workspace_folder_copy.to_dict())


def test_position():
    # Create our expected variables we'll construct tests with.
    expected_line = 77
    expected_character = 123

    # Test parsing position data
    position: Position = Position.from_dict({'line': expected_line, 'character': expected_character})
    assert position.line == expected_line and position.character == expected_character

    # Test round trip conversion of the position data
    position_copy = Position.from_dict(position.to_dict())
    assert position == position_copy
    assert json.dumps(position.to_dict()) == json.dumps(position_copy.to_dict())


def test_range():
    # Create our expected variables we'll construct tests with.
    expected_start = Position(123, 456)
    expected_end = Position(789, 100)

    # Test parsing range data
    range_item: Range = Range.from_dict({
        'start': expected_start.to_dict(),
        'end': expected_end.to_dict()
    })
    assert range_item.start == expected_start and range_item.end == expected_end

    # Test round trip conversion of the range data
    range_copy = Range.from_dict(range_item.to_dict())
    assert range_item == range_copy
    assert json.dumps(range_item.to_dict()) == json.dumps(range_copy.to_dict())


def test_location():
    # Create our expected variables we'll construct tests with.
    expected_uri = "/file/testpath/testuripath"
    expected_range = Range(Position(123, 456), Position(789, 100))

    # Test parsing location data
    location: Location = Location.from_dict({
        'uri': expected_uri,
        'range': expected_range.to_dict()
    })
    assert location.uri == expected_uri and \
           location.range == expected_range

    # Test round trip conversion of the location data
    location_copy = Location.from_dict(location.to_dict())
    assert location == location_copy
    assert json.dumps(location.to_dict()) == json.dumps(location_copy.to_dict())


def test_location_link():
    # Create our expected variables we'll construct tests with.
    expected_origin_selection_range = Range(Position(123, 456), Position(789, 100))
    expected_target_uri = "c:\\file\\origin.uri"
    expected_target_range = Range(Position(321, 654), Position(987, 1))
    expected_target_selection_range = Range(Position(132, 465), Position(798, 205))

    # Test parsing location link data
    location_link: LocationLink = LocationLink.from_dict({
        'originSelectionRange': expected_origin_selection_range.to_dict(),
        'targetUri': expected_target_uri,
        'targetRange': expected_target_range.to_dict(),
        'targetSelectionRange': expected_target_selection_range.to_dict()
    })
    assert location_link.origin_selection_range == expected_origin_selection_range and \
           location_link.target_uri == expected_target_uri and \
           location_link.target_range == expected_target_range and \
           location_link.target_selection_range == expected_target_selection_range

    # Test round trip conversion of the location data
    location_link_copy = LocationLink.from_dict(location_link.to_dict())
    assert location_link == location_link_copy
    assert json.dumps(location_link.to_dict()) == json.dumps(location_link_copy.to_dict())


def test_diagnostic_related_information():
    # Create our expected variables we'll construct tests with.
    expected_location = Location("/file/testpath/testuripath", Range(Position(123, 456), Position(789, 100)))
    expected_message = "testMessagePlaceholder"

    # Test parsing diagnostic related information
    diagnostic_related_info: DiagnosticRelatedInformation = DiagnosticRelatedInformation.from_dict({
        'location': expected_location.to_dict(),
        'message': expected_message
    })
    assert diagnostic_related_info.location == expected_location and diagnostic_related_info.message == expected_message

    # Test round trip conversion of the location data
    diagnostic_related_info_copy = DiagnosticRelatedInformation.from_dict(diagnostic_related_info.to_dict())
    assert diagnostic_related_info == diagnostic_related_info_copy
    assert json.dumps(diagnostic_related_info.to_dict()) == json.dumps(diagnostic_related_info_copy.to_dict())


def test_code_description():
    # Create our expected variables we'll construct tests with.
    expected_href = "testHrefString"

    # Test parsing code description
    code_description: CodeDescription = CodeDescription.from_dict({
        'href': expected_href
    })
    assert code_description.href == expected_href

    # Test round trip conversion of the location data
    code_description_copy = CodeDescription.from_dict(code_description.to_dict())
    assert code_description == code_description_copy
    assert json.dumps(code_description.to_dict()) == json.dumps(code_description_copy.to_dict())


def test_diagnostic():
    # Create our expected variables we'll construct tests with.
    expected_range = Range(Position(123, 456), Position(789, 100))
    expected_severity = DiagnosticSeverity.ERROR
    expected_code = "X9-01-07-1992"
    expected_code_description = CodeDescription("testHrefData")
    expected_source = "testSourceData"
    expected_message = "testMessageData"
    expected_tags = [DiagnosticTag.DEPRECATED, DiagnosticTag.UNNECESSARY]
    expected_related_info = [
        DiagnosticRelatedInformation(
            Location('locationUri', Range(Position(111, 222), Position(333, 444))), 'diagnosticRelatedInfo'
        ),
        DiagnosticRelatedInformation(
            Location('locationUri2', Range(Position(555, 666), Position(777, 888))), 'diagnosticRelatedInfo2'
        )
    ]
    expected_data = "testData"

    # Test parsing location link data
    diagnostic: Diagnostic = Diagnostic.from_dict({
        'range': expected_range.to_dict(),
        'severity': int(expected_severity),
        'code': expected_code,
        'codeDescription': expected_code_description.to_dict(),
        'source': expected_source,
        'message': expected_message,
        'tags': [int(diagnostic_tag) for diagnostic_tag in expected_tags],
        'relatedInformation': [related_info.to_dict() for related_info in expected_related_info],
        'data': expected_data
    })
    assert diagnostic.range == expected_range and \
           diagnostic.severity == expected_severity and \
           diagnostic.code == expected_code and \
           diagnostic.code_description == expected_code_description and \
           diagnostic.source == expected_source and \
           diagnostic.message == expected_message and \
           diagnostic.tags == expected_tags and \
           diagnostic.related_information == expected_related_info and \
           diagnostic.data == expected_data

    # Test round trip conversion of the location data
    diagnostic_copy = Diagnostic.from_dict(diagnostic.to_dict())
    assert diagnostic == diagnostic_copy
    assert json.dumps(diagnostic.to_dict()) == json.dumps(diagnostic_copy.to_dict())


def test_command():
    # Create our expected variables we'll construct tests with.
    expected_title = "testHrefString"
    expected_command = "testCommandString"
    expected_arguments = [
        {'A': 'OK', 'B': 'Hello!'},
        0,
        77,
        False
    ]

    # Test parsing command data
    command: Command = Command.from_dict({
        'title': expected_title,
        'command': expected_command,
        'arguments': expected_arguments
    })
    assert command.title == expected_title and \
           command.command == expected_command and \
           command.arguments == expected_arguments

    # Test round trip conversion of the location data
    command_copy = Command.from_dict(command.to_dict())
    assert command == command_copy
    assert json.dumps(command.to_dict()) == json.dumps(command_copy.to_dict())


def test_textedit():
    # Create our expected variables we'll construct tests with.
    expected_range = Range(Position(123, 456), Position(321, 654))
    expected_new_text = "testNewText"

    # Test parsing location link data
    text_edit: TextEdit = TextEdit.from_dict({
        'range': expected_range.to_dict(),
        'newText': expected_new_text
    })
    assert text_edit.range == expected_range and text_edit.new_text == expected_new_text

    # Test round trip conversion of the location data
    text_edit_copy = TextEdit.from_dict(text_edit.to_dict())
    assert text_edit == text_edit_copy
    assert json.dumps(text_edit.to_dict()) == json.dumps(text_edit_copy.to_dict())


def test_change_annotation():
    # Create our expected variables we'll construct tests with.
    expected_label = "testLabel"
    expected_needs_confirmation = False
    expected_description = "testDescription"

    # Test parsing location link data
    change_annotation: ChangeAnnotation = ChangeAnnotation.from_dict({
        'label': expected_label,
        'needsConfirmation': expected_needs_confirmation,
        'description': expected_description
    })
    assert change_annotation.label == expected_label and \
           change_annotation.needs_confirmation == expected_needs_confirmation and \
           change_annotation.description == expected_description

    # Test round trip conversion of the location data
    change_annotation_copy = ChangeAnnotation.from_dict(change_annotation.to_dict())
    assert change_annotation == change_annotation_copy
    assert json.dumps(change_annotation.to_dict()) == json.dumps(change_annotation_copy.to_dict())


def test_annotated_text_edit():
    # Create our expected variables we'll construct tests with.
    expected_range = Range(Position(123, 456), Position(321, 654))
    expected_new_text = "testNewText"
    expected_annotation_id = "testAnnotationId"

    # Test parsing location link data
    annotated_text_edit: AnnotatedTextEdit = AnnotatedTextEdit.from_dict({
        'range': expected_range.to_dict(),
        'newText': expected_new_text,
        'annotationId': expected_annotation_id
    })
    assert annotated_text_edit.range == expected_range and annotated_text_edit.new_text == expected_new_text

    # Test round trip conversion of the location data
    annotated_text_edit_copy = AnnotatedTextEdit.from_dict(annotated_text_edit.to_dict())
    assert annotated_text_edit == annotated_text_edit_copy
    assert json.dumps(annotated_text_edit.to_dict()) == json.dumps(annotated_text_edit_copy.to_dict())