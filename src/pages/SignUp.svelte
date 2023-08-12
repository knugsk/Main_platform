<script lang="ts">
    import "./SignUp.scss";

    import { pop } from "svelte-spa-router";

    let name = "";

    let student_code = "";
    let error_student_code = false;
    $: {check_student_code(student_code)}

    let password = "";
    let error_pw = false;
    $: {check_password(password)}

    let re_password = "";
    let error_re_pw = false;
    $: {check_re_password(re_password)}

    const check_student_code = (sc)=> {
        if(student_code){
            error_student_code = !student_code.match(/^[0-9]{10}$/);
        }
    }

    const check_password = (pw) => {
        if(password){
            error_pw = !password.match(/^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,16}$/);
        }
    }

    const check_re_password = (rpw) => {
        if(password === re_password ){
            error_re_pw = false;
        }	else{
            error_re_pw = true;
        }
    }	
</script>

<div class="container_signup">
    <h1>가입 신청</h1>
    <div class="">
        <input 
            type="text"
            bind:value={name}
            placeholder="성명"
        >
    </div>
    <div class="box_student_code">
        <input 
            type="text"
            bind:value={student_code}
            placeholder="학번"
        >
        {#if error_student_code}
            <p class="warning">학번 형식이 올바르지 않습니다.</p>
        {/if}
    </div>
    <div>
        <input type="password"
            bind:value={password}
            placeholder="영문+숫자+특수문자 8~16자리(특수문자()괄호는 사용불가)"
        >
        {#if error_pw}
            <p class="warning">비밀번호 형식이 올바르지 않습니다.</p>
        {/if}
    </div>
    <div>
        <input type="password"
            placeholder="패스워드를 다시 입력해주세요."
            bind:value={re_password}
        >
        {#if error_re_pw}
            <p class="warning">입력값이 일치하지 않습니다.</p>
        {/if}
    </div>
    <div class="box_btn">
        <button class="btn_cancle" on:click={() => pop()}>
            취소
        </button>
        <button class="btn_book">
            신청
        </button>
    </div>
</div>