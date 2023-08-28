<script lang="ts">
    import "./MainPage_Contents.scss";

    import SubNav_ProjectNav from "@/components/SubNav_ProjectNav.svelte";
    
    import { get_contents } from "query";
    import koreantime from "@/lib/datetime";
    import { push } from "svelte-spa-router";

    export let params: { contents_id: string } = { contents_id: "" }

    let data: any = null;
    let title: string = "error";
    let page: number = 1;
    let max_page: number = 1;

    const get_data = async (contents_id: string) => {
        let id = 1;

        switch (contents_id) {
            case "notice":
                id = 1;
                title = "공지사항";
                break;
            case "project":
                id = 2;
                title = "프로젝트";
                break;
            case "job":
                id = 4;
                title = "구인/구직";
                break;
            case "budget":
                id = 3;
                title = "예산 신청";
                break;
            default:
                break;
        }

        get_contents(id)
            .then(res => {
                if(data !== null || data !== undefined) {
                    if (Array.isArray(res)) {
                        data = [...res].reverse();
                    }
                }
            }).catch(err => {
                console.log(err);
            });
    }
    
    $: data = get_data(params.contents_id);
</script>

<div class="container_contents">
    {#if params.contents_id !== "notice"}
        <SubNav_ProjectNav />
    {/if}
    <h1 class="title_contents">{title}</h1>
    <div class="container_bar">
        {#if data !== null && data !== undefined}
            {#each data as content, index }
                <button class={"bar_content" + (index == 0 ? " first" : "")} on:click={() => {push(`/contents/content/${content.id}`);}}>
                    <p class="text_bar title">{content.title}</p>
                    <p class="text_bar author">{`작성자: ${content.author.first_name} ${content.author.last_name}`}</p>
                    <p class="text_bar date">{koreantime(content.published_date)}</p>
                </button>
            {/each}
            {#if data.length === 0}
                <div class="box_non_contents">
                    <h1>게시글이 없어요!</h1>
                </div>
            {/if}
        {/if}
    </div>
    <div class="pagination">

    </div>
</div>

