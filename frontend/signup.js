// 63강 생성
const form = document.querySelector('#signup-form');

const checkPassword = () => {
    const formData = new FormData(form);
    const password1 = formData.get('password');
    const password2 = formData.get('password2');
    if (password1 === password2) {
        return true;
    } else return false;
};

const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const sha256Password = sha256(formData.get('password'));
    formData.set('password', sha256Password);

    const div = document.querySelector('#info');

    if (checkPassword()){
        const res = await fetch('/signup', {
            method : 'post',
            body : formData,
        });
        const data = await res.json();
        if (data === '200') {
            // 64강 추가 - 로그인페이지로 이동
            alert('회원가입에 성공했습니다');
            window.location.pathname = '/login.html';
            // 64강 추가 - 로그인페이지로 이동 end
        }
    } else {
        div.innerText = '비밀번호가 같지 않습니다';
        div.style.color = 'red';
    }
};

form.addEventListener('submit', handleSubmit);