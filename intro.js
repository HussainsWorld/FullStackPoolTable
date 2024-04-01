
$(document).ready(function() {
    $('#player-form').submit(function(event) {
        event.preventDefault();
        const player1Name = $('#player1').val();
        const player2Name = $('#player2').val();
        
        // Make a POST request to set player names on the server
        $.ajax({
            url: '/set_player_names',
            type: 'POST',
            data: { playerName1: player1Name, playerName2: player2Name },
            success: function(data, status) {
                // Redirect to the game page after setting player names
                window.location.href = 'game.html';
            },
            error: function(xhr, status, error) {
                // Handle error if needed
                console.error('Error occurred:', error);
            }
        });
    });
});

