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
    if (confirm("Bạn chắc chắn lưu vé chưa?") == true)
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
            alert(data.message);
        });

}
function pay(){
    if (confirm("Bạn chắc chắn thanh toán chưa?") == true)
        fetch('api/pay', {
            'method': 'post',
             'headers': {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(res =>res.json()).then(data =>{
            alert(data.message);
            location.reload();
        }).catch(err => console.log(err));

}


