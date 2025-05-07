// 64강 생성
const form = document.querySelector('#login-form');

// 65강 추가
// 66강 주석처리
// let accessToken = null;

const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const sha256Password = sha256(formData.get('password'));
    formData.set('password', sha256Password);
    
    const res = await fetch('/login', {
        method : 'post',
        body : formData,
    });
    const data = await res.json();
    // 65강 - 받아온 데이터 액세스 토큰으로 업데이트
    // 66강 - 로컬스토리지&세션스토리지에 저장하기 Start
    const accessToken = data.access_token;
    window.localStorage.setItem('token', accessToken);
    alert('로그인 되었습니다');

    window.location.pathname = '/';
    // window.sessionStorage.setItem('token', accessToken); // 66강 - 로컬스토리지&세션스토리지에 저장하기 End

    // 65강 - 로그인 되었다는 알림
    // 66강 주석처리
    // const infoDiv = document.querySelector('#info');
    // infoDiv.innerText = '로그인 되었습니다';



    // 65강 -  상품 데이터 잘 가져오는지 확인하기 Start
    // const btn = document.createElement('button');
    // btn.innerText = '상품 가져오기';
    // btn.addEventListener('click', async () => {
    //     const res = await fetch('/items', {
    //         headers : {
    //             'Authorization' : `Bearer ${accessToken}`,
    //         },
    //     });
    //     const data = await res.json();
    //     console.log(data);
    // });
    // infoDiv.appendChild(btn); // 65강 -  상품 데이터 잘 가져오는지 확인하기 End

    
    
    // 64강 - 로그인 OK인지 아닌지
    // if (res.status === 200) {
    //     alert('로그인에 성공했습니다');
    //     window.location.pathname = '/';
    // }else if (res.status === 401){
    //     alert('ID 혹은 Password가 틀렸습니다');
    // }// 64강 - 로그인 OK인지 아닌지 end
};

form.addEventListener('submit', handleSubmit);