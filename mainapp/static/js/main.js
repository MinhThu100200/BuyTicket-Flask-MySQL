function addToDetail(id){
    fetch('/api/detail', {
        'method': 'post',
        'body': JSON.stringify({
            'id': id

        }),
        'headers': {
            'Content-Type': 'application/json'

        }

    }).then(res =>res.json()).then(data =>{
            console.log(data);
    });
}
function addToCart(id){
    var price = document.getElementById('price');
    fetch('api/cart', {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'price': price.value

        }),
         'headers': {
            'Content-Type': 'application/json',
            'Accept': 'application/json'

        }
    }).then(res =>res.json()).then(data =>{
        console.log(data);
    });

}

