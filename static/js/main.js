// Fonctions communes à toutes les pages
document.addEventListener('DOMContentLoaded', function() {
    // Activer tous les tooltips Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
    
    // Fermer les alertes après 5 secondes
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            if (alert && typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                if (bsAlert && typeof bsAlert.close === 'function') {
                    bsAlert.close();
                }
            }
        });
    }, 5000);

    // Simplifier la sélection de l'élément d'enchère
    const bidForm = document.getElementById('bid-form');
    if (bidForm) {
        // Récupérer l'ID de l'enchère à partir du formulaire ou de l'attribut data
        const auctionId = bidForm.querySelector('input[name="auction_id"]').value || 
                          document.querySelector('[data-auction-id]').dataset.auctionId;
        
        if (auctionId) {
            // Mettre à jour le prix minimum (enchères inversées)
            updateMinimumBid(auctionId);
            setInterval(() => updateMinimumBid(auctionId), 3000);
            
            // Gérer la soumission du formulaire
            bidForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(bidForm);
                
                // Afficher un petit message de chargement
                const submitBtn = bidForm.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Traitement...';
                
                fetch('/bids', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Afficher un message de succès
                        alert('Enchère placée avec succès!');
                        // Recharger la page pour voir les mises à jour
                        window.location.reload();
                    } else {
                        // Afficher l'erreur
                        alert('Erreur: ' + data.message);
                        // Réactiver le bouton
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalBtnText;
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    alert('Une erreur est survenue lors de la soumission de l\'enchère.');
                    // Réactiver le bouton
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                });
            });
        }
    }

    // Mettre à jour automatiquement le prix maximum toutes les 3 secondes
    const auctionElement = document.querySelector('[data-auction-id]');
    if (auctionElement) {
        const auctionId = auctionElement.dataset.auctionId;
        updateMinimumBid(auctionId);
        setInterval(() => updateMinimumBid(auctionId), 3000);
    }
});

// Supprimer la fonction updateMinimumBid qui n'est pas nécessaire

// Remplacer updateMaximumBid par updateMinimumBid
function updateMinimumBid(auctionId) {
    fetch(`/api/auction/${auctionId}/min-bid`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Mettre à jour l'affichage du prix minimum
                const minBidElement = document.getElementById('min-bid-amount');
                if (minBidElement) {
                    minBidElement.textContent = data.formatted_min_bid;
                }
                
                // Mettre à jour les attributs du champ d'enchère
                const bidInput = document.getElementById('amount');
                if (bidInput) {
                    bidInput.max = data.min_bid; // La valeur max du champ est le prix minimum actuel
                    bidInput.placeholder = `Max: ${data.formatted_min_bid}`;
                }
            }
        })
        .catch(error => console.error('Erreur lors de la récupération du prix minimum:', error));
}