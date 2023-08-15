<script lang="ts">
    import "./SubPage_SignIn.scss";

    import Modal from "@/components/Modal.svelte";

    import { pop } from "svelte-spa-router";
    import { sign_in } from "query";

    let student_code = "";
    let password = "";

    let showModal = false;
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
        <button class="btn_book" on:click={async () => {
            await sign_in(student_code, password).then(success => {
                if(success) {
                    pop();
                }
                else {
                    showModal = true;
                }
            });
        }}>
            로그인
        </button>
    </div>
</div>

<Modal bind:showModal>
	<h2 slot="header">
        로그인 에러
	</h2>

	<ol class="definition-list">
        <li>아직 등록되지 않거나 일치하지 않는 정보입니다.</li>
		<li>학번과 비밀번호를 다시 확인해주세요.</li>
	</ol>
</Modal>