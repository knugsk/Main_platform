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
        <div class="board_content">
            <div class="box_main">
                <div class="box_title">
                    <div class="title">
                        <h1>{data.title}</h1>
                    </div>
                    <div class="author">
                        <p>{data.author}</p>
                    </div>
                </div>
                <div class="content">
                    <p>{data.body}</p>
                </div>
            </div>
            <div class="files">

            </div>
        </div>
        <div class="board_comment">
            <div class="box_comment">
                
            </div>
        </div>
    {:else}
        <h1>헉 페이지를 못 찾겠어요!</h1>
    {/if}
</div>