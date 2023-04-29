document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('#submitBtn').addEventListener('click', () => chat_ajax());

});

function chat_ajax(){

    let text = document.querySelector('#userText').value
    let chatCard = document.querySelector('#chatCard')
    chatCard.innerHTML += `
    <div class="card-body bg bg-primary">
        <p class="card-title font-weight-light" style="white-space: pre-wrap;">${text}</p>
    </div>
    `
    console.log(text)

    // Clear input:
    document.querySelector('#userText').value = null

    var loading = document.querySelector('#loading')
    loading.innerHTML = `
    <strong>Loading...</strong>
    <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
    `

    $.ajax({
        type: 'POST',
        url: '/ajax/',
        data: {
            'text': text
        },
        success: (res)=> {
            let response = res.data
            chatCard.innerHTML += `
            <div class="card-body bg bg-light text-dark">
                  <p class="card-title font-weight-light" style="white-space: pre-wrap;">${response}</p>
            </div>
            `
            loading.innerHTML = ''
        },
        error: ()=> {
            console.log("There Was An Error!")
        }
    })
}