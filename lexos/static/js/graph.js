let graph_id;

/**
 * Creates a Plotly graph.
 * @param {string} url: The URL to send the request for the Plotly HTML to.
 */
function create_graph(url){

    // Add the loading overlay to the graph container
    start_loading("#graph-container");

    // Send the request for the Plotly graph HTML
    send_ajax_form_request(url)
    .done(function(response){

        // Add the Plotly graph HTML
        let graph_element = $(`<div id="graph" class="hidden"></div>`)
            .html(response)
            .appendTo("#graph-container");

        // Get the Plotly graph ID
        graph_id = graph_element.find(".js-plotly-plot").attr("id");

        // Update the graph size
        update_graph_size();
        $(window).resize(update_graph_size);

        // Remove the loading overlay and show the graph
        finish_loading("#graph-container", "#graph");
    });
}

/**
 * Updates the size of the graph to fit its container.
 */
function update_graph_size(){

    // Get the graph container element
    let graph_container_element = $("#graph-container");

    // Resize the graph to fit the graph container
    Plotly.relayout(graph_id, {width: graph_container_element.width(),
        height: graph_container_element.height()});
}
