// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Event listener for processing files
    document.querySelectorAll('.process-btn').forEach(button => {
        button.addEventListener('click', function() {
            const fileId = this.getAttribute('data-file-id');

            fetch('/process', {  // Replace with your actual processing URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'  // Ensure CSRF token is sent
                },
                body: JSON.stringify({ file_id: fileId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    document.getElementById('message').innerText = data.message;
                    location.reload();  // Reload the page to see updated statuses
                } else {
                    alert('Erreur lors du traitement : ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erreur lors du traitement.');
            });
        });
    });

    // Event listener for deleting files
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const fileId = this.getAttribute('data-file-id');

            if (confirm('Êtes-vous sûr de vouloir supprimer ce fichier ?')) {
                fetch(`/delete/${fileId}`, {  // Replace with your actual deletion URL
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'  // Ensure CSRF token is sent
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        document.getElementById('message').innerText = data.message;
                        location.reload();  // Reload the page to see updated statuses
                    } else {
                        alert('Erreur lors de la suppression : ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Erreur lors de la suppression.');
                });
            }
        });
    });
});
