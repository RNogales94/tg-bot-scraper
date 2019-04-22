
function loadProducts(){
    fetch('/api/products?limit=80&origin=RNogales')
    .then(response => response.json())
    .then(products => {
        let products_panel = document.getElementById('offers-section');
        for (product of products){
            p = new Product(product)
            console.log(p.shortDescription)
            products_panel.appendChild(p.toElement())
        }
    })
    .catch(error => console.log('Error' + error))
}



