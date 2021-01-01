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

