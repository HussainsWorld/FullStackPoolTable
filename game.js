// Define a flag variable to track whether the code has been executed
let svgContentLoaded = false;

// Execute the code only when the DOM is fully loaded
$(document).ready(function() {

    svgContentLoaded = true;
    $('#svg-container').hide();
    // Get player names from localStorage
    // Get player names from input elements
    const player1Name = $('#player1').val();
    const player2Name = $('#player2').val();

    // Display player names on the left and right sides of the pool table
    $('#player1-name').text(player1Name);
    $('#player2-name').text(player2Name);

    $.ajax({
        url: '/get_svg_content',
        type: 'POST',
        dataType: 'text',
        success: function(svgContent) {
            console.log(svgContent); 
            $('#svg-container').html(svgContent);
            $('#svg-container').show();
            attachEventHandlers();
        },
        error: function(xhr, status, error) {
            console.error('Error occurred:', error); // Log the error message
        }
    });
    // }
});

function attachEventHandlers() {
    let isDragging = false;
    let startPoint = {};
    let line = null;
    document.querySelector('#svg-container svg'); 

    function screenToSVG(x, y, svgElement) {
        let point = svgElement.createSVGPoint();
        point.x = x;
        point.y = y;
        return point.matrixTransform(svgElement.getScreenCTM().inverse());
    }

    $('#cue-ball').on('mousedown', function(evt) {
        const svgElement = $('#svg-container svg')[0];
        svgElement.getBoundingClientRect();
        startPoint = screenToSVG(evt.clientX, evt.clientY, svgElement);
        isDragging = true;
        line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        $(line).attr({
            'x1': startPoint.x,
            'y1': startPoint.y,
            'x2': startPoint.x,
            'y2': startPoint.y,
            'stroke': 'red',
            'stroke-width': 5,
            'visibility' : 'visible'
        });
        $(svgElement).append(line);
        evt.preventDefault();
    });

    $(window).on('mousemove', function(evt) {
        if (!isDragging) return;
        const svgElement = $('#svg-container svg')[0];
        const currentPoint = screenToSVG(evt.clientX, evt.clientY, svgElement);
        $(line).attr({'x2': currentPoint.x, 'y2': currentPoint.y});
    });
    
    $(window).on('mouseup', function(evt) {
        if (!isDragging) return;
            isDragging = false;
            const svgElement = $('#svg-container svg')[0];
            const release = screenToSVG(evt.clientX, evt.clientY, svgElement);
            let xV = release.x - startPoint.x;
            let yV = release.y - startPoint.y;

            $(line).remove();

            $.ajax({
                url: '/submit_shot',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 
                    dx: xV,
                    dy: yV
                }),
                success: function(data) {
                    console.log('Shot processed:', data);
                    for (let frame of data.frames) {
                        $('#svg-container').html(frame);
                        $('#svg-container').show();
                    }
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            }); 
        });
}


$(document).ready(function() {
    simulateAndDisplayShot();
});