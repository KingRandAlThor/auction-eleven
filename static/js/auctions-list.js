document.addEventListener('DOMContentLoaded', function() {
    console.log('Page des enchères chargée');
    
    // Animation d'entrée des cartes
    const auctionCards = document.querySelectorAll('.auction-card');
    if (auctionCards.length > 0) {
        auctionCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });
    }
    
    // Mettre à jour les compteurs de temps restant (optionnel)
    // Cette fonction pourrait être améliorée pour mettre à jour les compteurs sans recharger la page
    function checkAuctionStatus() {
        const auctionElements = document.querySelectorAll('[data-auction-id]');
        
        auctionElements.forEach(element => {
            const auctionId = element.dataset.auctionId;
            
            // Vous pouvez ajouter une requête AJAX ici pour vérifier le statut d'une enchère
            // Exemple:
            /*
            fetch(`/api/auction/${auctionId}/status`)
                .then(response => response.json())
                .then(data => {
                    // Mettre à jour l'affichage en fonction des données reçues
                });
            */
        });
    }
    
    // Exécuter une vérification toutes les minutes (optionnel)
    // setInterval(checkAuctionStatus, 60000);
});