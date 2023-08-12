<script lang="ts">
    import "./SignIn.scss";

    import { pop } from "svelte-spa-router";

    let student_code = "";
    let password = "";

</script>

<div class="container_signin">
    <h1>로그인</h1>
    <div class="box_student_code">
        <input 
            type="text"
            bind:value={student_code}
            placeholder="학번"
        >
    </div>
    <div>
        <input type="password"
            bind:value={password}
            placeholder="비밀번호"
        >
    </div>
    <div class="box_btn">
        <button class="btn_cancle" on:click={() => pop()}>
            취소
        </button>
        <button class="btn_book">
            로그인
        </button>
    </div>
</div>