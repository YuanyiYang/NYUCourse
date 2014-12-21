function questionVote(option){
    var formData = document.forms['questionVoteForm']
    //$.post("/vote", {type: 'question',qId: formData['qid']['value'],user: formData['user']['value'],result: formData['result']['value']})
    if(option){
        result = 'up'
    } else {
        result = 'down'
    }
    $.ajax({
        url: '/vote',
        type: 'POST',
        dataType: 'json',
        data: {'type': 'question',
                'qId': formData['qid']['value'],
                'user': formData['user']['value'],
                'result': result
                },
    })
    .always(function() {
        window.location='/viewQuestion?qId=' + formData['qid']['value']
    });
};
