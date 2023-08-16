<script lang="ts">
    import "./MainPage_Intro.scss";

    import { is_login, access_token } from "@/lib/store";
    import { sign_out } from "query";
    import { push, replace } from "svelte-spa-router";

    import Modal_SignInError from "@/components/Modal_SignInError.svelte";
    let showModal = false;
</script>

<div class="container_intro">
    <div class="container_introduction">
        <img class="logo" alt="logo" src="logo/logo.svg" />
        <div class="box_introduction">
            <p>경북대학교</p>
            <h1>현대시각문화연구회</h1>
            <h3>현대시각문화연구회, 약칭 현시연은</h3>
            <h3>서브컬쳐에 관심있는 학생들이 모여 교류하고,</h3>
            <h3>다양한 창작활동을 진행하는 학술동아리입니다.</h3>
        </div>
    </div>
    <div class="container_auth">
        {#if $is_login === false}
            <a class="btn_sign" href="#/sign-up" on:click={() => push("/sign-up")}>
                <span>
                    <div class="black">
                        회원가입
                    </div>
                </span>
            </a>
            <a class="btn_sign" href="#/sign-in"  on:click={() => push("/sign-in")}>
                <span>
                    <div class="white">
                        로그인
                    </div>
                </span>
            </a>
        {:else}
            <a class="btn_sign" href="#/" on:click={() => {
                sign_out();
            }}>
                <span>
                    <div class="black">
                        로그아웃
                    </div>
                </span>
            </a>
            <!-- <a class="btn_sign" href="#/my_page"  on:click={() => showModal = true}>
                <span>
                    <div class="white">
                        내 정보
                    </div>
                </span>
            </a>  -->
        {/if}
    </div>
    <img class="knu_logo" alt="logo" src="logo/knu_logo.jpg" />
</div>

<Modal_SignInError bind:showModal>
	<h2 slot="header">
        Comming Soon..
	</h2>

	<ol class="definition-list">
        <li>곧 돌아옵니다.</li>
	</ol>
</Modal_SignInError>