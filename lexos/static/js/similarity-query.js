$(function(){

    // Display the loading overlay for the "Comparison Document" and
    // "Similarity Table" sections
    start_loading("#comparison-document-section-body, #table");

    // Initialize the legacy form inputs and create the similarity table
    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});

/**
 * Initialize the legacy form inputs and create the similarity table.
 * @param {string} response: The response from the "/active-file-ids" request.
 */
function initialize(response){

    // Initialize the legacy form inputs. If there are no active documents,
    // display "No Active Documents" text and return
    if(!initialize_legacy_inputs(response)){
        add_text_overlay("#comparison-document-section-body, #table",
            "No Active Documents");
        return;
    }

    // Otherwise, parse the response
    let documents = Object.entries(parse_json(response));

    // Enable the "Comparison Document" section's "Select" button
    let select_button_element = $("#select-button");
    select_button_element.removeClass("disabled");

    // Set the comparison document to the first document
    let first_document = documents[0];
    $("#comparison-document-input").val(first_document[0]);

    $(`<h3 id="comparison-document-text" class="hidden"></h3>`)
        .appendTo("#comparison-document-section-body")
        .text(first_document[1]);

    // Remove the loading overlay from the "Comparison Document" section and
    // fade in the comparison document name
    finish_loading("#comparison-document-section-body",
        "#comparison-document-text");

    // Register the popup creation callback for the "Comparison Document"
    // section's "Select" button
    select_button_element.click(function(){
        create_radio_options_popup("Comparison Document",
            "comparison-document", "#comparison-document-text",
            "#comparison-document-input", documents
        );
    });

    // Create the similarity table
    send_ajax_form_request("similarity-query/table")
        .done(create_similarity_table);

    // If the "Generate" button is pressed, recreate the similarity table
    $("#generate-button").click(function(){
        if(!validate_analyze_inputs()) return;
        start_loading("#table", "#generate-button");
        send_ajax_form_request("similarity-query/table")
            .done(create_similarity_table);
    });
}


function create_similarity_table(response){

    let table_data = parse_json(response);

    // Create the layout
    $(`
        <div id="table-head" class="hidden">
            <h3 class="table-cell">Document</h3>
            <h3 class="table-cell">Cosine Similarity</h3>
        </div>
        <div id="table-body" class="hidden"></div>
    `).appendTo("#table");

    // Create the body
    let table_body = $("#table-body");
    for(const row of table_data){

        // Create a row element
        let row_element = $(`
            <h3 class="table-row"></h3>
        `).appendTo(table_body);

        // Populate the row
        for(const cell of row){
            let cell_element = $(`
                <h3 class="table-cell"></h3>
            `).appendTo(row_element);

            cell_element.text(cell);
        }
    }

    // Remove the loading overlay, fade in the table, and enable the
    // "Generate" button
    finish_loading("#table", "#table-head, #table-body", "#generate-button");
}
