<script lang="ts">
    import "./SubPage_Content.scss";

    import { beforeUpdate } from "svelte";
    import { get_content } from "query";

    export let params: { content_id: string } = { content_id: "" }

    let data: any = null;

    const get_data = async () => {
        get_content(params.content_id)
            .then(res => {
                if(data !== null || data !== undefined) data = res;
            }).catch(err => {
                console.log(err);
            });
    }

    beforeUpdate(async () => {
        await get_data();
    });

</script>

<div class="container_content">
    {#if data !== null && data !== undefined}
        <div class="container_left">
            <button class="nav_content" on:click={() => {}}>
                <p class="text_titleOrAuthor">{"< 뒤로가기"}</p>
            </button>
            <div class="board_files">
                
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
                    <p>{data.body}</p>
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
        </div>
    {:else}
        <h1>헉 페이지를 못 찾겠어요!</h1>
    {/if}
</div>