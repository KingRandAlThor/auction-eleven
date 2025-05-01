document.addEventListener('DOMContentLoaded', function() {
    // Formulaire de mise
    const bidForm = document.getElementById('bid-form');
    if (bidForm) {
        bidForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitBid();
        });
    }
});

// Fonction pour soumettre une mise via l'API
async function submitBid() {
    const bidAmount = document.getElementById('bid-amount').value;
    const auctionId = document.getElementById('auction-id').value;
    const bidResult = document.getElementById('bid-result');
    
    // Validation côté client
    if (!bidAmount || isNaN(bidAmount) || parseFloat(bidAmount) <= 0) {
        bidResult.innerHTML = `<div class="alert alert-danger">Veuillez entrer un prix valide</div>`;
        return;
    }
    
    // Afficher l'indicateur de chargement
    bidResult.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Chargement...</span>
            </div>
            <p class="mt-2">Traitement de votre mise...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/bids', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                auction_id: auctionId,
                price: bidAmount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            bidResult.innerHTML = `
                <div class="alert alert-success">
                    <i class="bi bi-check-circle me-2"></i>
                    ${data.message}
                </div>
            `;
            document.getElementById('bid-form').reset();
            
            // Mettre à jour le solde affiché
            const tokenBalance = document.querySelector('.badge.bg-success');
            if (tokenBalance) {
                tokenBalance.textContent = `${data.new_balance} jetons`;
            }
            
            // Recharger la page après 2 secondes pour voir les mises à jour
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            bidResult.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-circle me-2"></i>
                    ${data.message}
                </div>
            `;
        }
    } catch (error) {
        console.error('Erreur:', error);
        bidResult.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle me-2"></i>
                Une erreur est survenue lors de la communication avec le serveur
            </div>
        `;
    }
}