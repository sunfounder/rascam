window.onload = () => {
    let cameraBtn = document.getElementById('btn');
    let cameraVideo = document.getElementById('camera_video');
    let photo = document.getElementById('photo');
    let photo_img = document.getElementById('photo_img');
    let share = document.getElementById('share');
    let close = document.getElementById('close');
    let toolTip = document.getElementById('tooltip');
    let lock = true;
    let lock2 = true;
    let imageTimer = null;
    var count = 0;
    cameraBtn.onclick = () => {
        clearTimeout(timer);
        cameraBtn.classList.add('camera_btn_transfrom');
        var timer = setTimeout(()=> {
            cameraBtn.classList.remove('camera_btn_transfrom');
        }, 100)
        reqSocket.send(JSON.stringify({'TA':'on'}));
        clearInterval(imageTimer);
        imageTimer = setInterval(()=> {
            if (count > 5) {
                count = 0;
                clearInterval(imageTimer);
            }
            photo.style.display = 'block';
            photo_img.src = location.href + `image/temp.jpg?t=${Math.round((Math.random()*10000))}`
            ++count;
        },700)
    }

    close.onclick = () => {
        photo.style.display = 'none';
        clearInterval(imageTimer);
        count = 0;
    }

    share.onclick = () => {
        toolTip.style.display = 'block';
        reqSocket.send(JSON.stringify({'SH':'on'}));
    }

    let reqSocket = new WebSocket(`ws://${location.hostname}:8765`);

    reqSocket.onopen = () => {
        console.log('reqSocket connect open...');
    }

    reqSocket.onmessage = (event) => {
        console.log(event);
    }

    reqSocket.onerror = () => {
        console.log('8765错误');
    }

    let resSocket = new WebSocket(`ws://${location.hostname}:8766`);

    resSocket.onopen = () => {
        console.log('resSocket connect open...');
    }

    resSocket.onmessage = (event) => {
        console.log(event);
        var data = JSON.parse(event.data);
        // console.log(data);
        if (data.AD && lock) {
            cameraVideo.src = data.AD;
            lock = false;
        }
        if (data.PD == 'Successful' && lock2) {
            toolTip.innerHTML = 'Share Successful...'
            lock2 = false;
            setTimeout( () => {
                toolTip.innerHTML = 'Shareing...'
                toolTip.style.display = 'none' 
                lock2 = true
            },1000)
        }
        if (data.PD == 'failed' && lock2) {
            toolTip.innerHTML = 'Share Failed...'
            lock2 = false;
            setTimeout( () => {
                toolTip.innerHTML = 'Shareing...'
                toolTip.style.display = 'none' 
                lock2 = true
            },1500)
        }
        // cameraVideo.src = data.AD;
    }

    resSocket.onerror = () => {
        console.log('8766错误');
    }
}