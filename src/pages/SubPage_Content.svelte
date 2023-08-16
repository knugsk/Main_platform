<script lang="ts">
    import "./SubPage_Content.scss";

    import { afterUpdate, onMount } from "svelte";
    import { get_content } from "query";
    import { pop } from "svelte-spa-router";
    import { deflateRaw } from "zlib";

    export let params: { content_id: string } = { content_id: "" }

    let data: any = null;

    const get_data = async (content_id: string) => {
        get_content(content_id)
            .then(res => {
                if(data !== null || data !== undefined) data = res;
                console.log(data);
            }).catch(err => {
                console.log(err);
            });
    }

    $: data = get_data(params.content_id)

    function filterImages(arr: any) {
        return arr.filter((item: any) => {
            const lowerCaseItem = item.toLowerCase();
            return lowerCaseItem.endsWith('.png') || lowerCaseItem.endsWith('.jpeg') || lowerCaseItem.endsWith('.jpg');
        });
    }
</script>

<div class="container_content">
    {#if data !== null && data !== undefined && data.comments !== null && data.comments !== undefined}
        <div class="container_left">
            <button class="nav_content" on:click={() => {pop();}}>
                <p class="text_titleOrAuthor">{"< 뒤로가기"}</p>
            </button>
            <div class="board_files">
                {#each filterImages(data.files) as file, index}
                    <div class="card_comment">
                        <p>file</p>
                    </div>
                {/each}
            </div>
        </div>
        <div class="board_content">
            <div class="box_main">
                <div class="box_titleAndAuthor">
                    <div class="box_title">
                        <p class="text_titleOrAuthor">{data.title}</p>
                    </div>
                    <div class="box_author">
                        <p class="text_titleOrAuthor">{data.author}</p>
                    </div>
                </div>
                <div class="box_content">
                    <p class="box_content_text">
                        {data.body}
                    </p>
                </div>
            </div>
        </div>
        <div class="board_comment">
            <div class="box_comment">
                {#each data.comments as comment, index}
                    <div class="card_comment">
                        <p class="text_comment">
                            작성자: {comment.author}
                        </p>
                        <p class="text_comment">
                            {comment.author}
                        </p>
                    </div>
                {/each}
            </div>
            <div class="box_send_comment">
                <textarea class="textarea_comment"/>
                <button class="btn_send_comment" />
            </div>
        </div>
    {:else}
        <h1>헉 페이지를 못 찾겠어요!</h1>
    {/if}
</div>