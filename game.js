let scores = {
    playerx: 0,
    cpu: 0,
    draws: 0
};

let playerx = 'X';
let cpu = 'O';
let currentPlayer = playerx;
let tic = ['', '', '', '', '', '', '', '', ''];
let arrayPattern = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
    [0, 4, 8], [2, 4, 6] // Diagonals
];

function showAlertWithTimeout(message, timeout) {
    alert(message);
    setTimeout(function() {
        // Close the alert after the specified timeout
        document.querySelector('.alert').style.display = 'none';
    }, timeout);
}

function handleMove(index) {
    if (tic[index] === '') {
        tic[index] = currentPlayer;
        document.getElementById('tic').children[index].innerText = currentPlayer;
        if (checkWinner(playerx)[0]) {
            setTimeout(resetGame, 1000);
            setTimeout(alert(`Player ${playerx} wins!`),600);
            scores.playerx++;
            return;
        }
        if (checkWinner(cpu)[0]) {
            setTimeout(resetGame, 1000);
            setTimeout(alert(`Player ${cpu} wins!`),600)
            scores.cpu++;
            return;
        }

        if (tic.every(tbox => tbox !== '')) {
            setTimeout(resetGame, 1000);
            setTimeout(alert('It\'s a draw!'),600);
            scores.draws++;
            return;
        }
        currentPlayer = currentPlayer === playerx ? cpu : playerx;
        if (currentPlayer === cpu) {
            setTimeout(computerMove, 600);
        }
    }
}

function checkWin(player) {
    // Define the winning patterns (rows, columns, diagonals)
    const patterns = arrayPattern;

    // Check each winning pattern
    for (let pattern of patterns) {
        const [a, b, c] = pattern;
        if (tic[a] === player && tic[b] === player && tic[c] === player) {
            return true; // Player has won
        }
    }

    return false; // No win found
}


function checkWinner(player) {
    // Define the winning patterns (rows, columns, diagonals)
    const patterns = arrayPattern;

    // Check each winning pattern
    for (let pattern of patterns) {
        const [a, b, c] = pattern;
        if (tic[a] === player && tic[b] === player && tic[c] === player) {
            return [true, pattern]; // Player has won
        }
    }

    return [false, null]; // No win found
}


function computerMove() {
    boardStr = [tic.slice(0,3), tic.slice(3, 6), tic.slice(6, 9)]
    board = boardStr.map(x => x.map(y => { 
        if (y == 'X') return 1;
        if (y == 'O') return -1;
        if (y.length == 0 || y == '') return 0;
    }))
    if (currentPlayer === cpu) {
        const formData = new FormData();
        formData.append("board", JSON.stringify(board));
        formData.append("maximizing", "false");

        fetch('http://127.0.0.1:5000/play', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const index = (data.move[0] * 3) + data.move[1];
            handleMove(index);
        });
    }
}

function resetGame() {
    currentPlayer = playerx;
    tic = ['', '', '', '', '', '', '', '', ''];
    document.getElementById('tic').childNodes.forEach(tbox => tbox.innerText = '');
    updateScores();
  }


  function updateScores() {
    document.getElementById('playerx-wins').textContent = scores.playerx;
    document.getElementById('cpu-wins').textContent = scores.cpu;
    document.getElementById('draws').textContent = scores.draws;
}

document.getElementById('restart-button').addEventListener('click', function() {
    location.reload();
});