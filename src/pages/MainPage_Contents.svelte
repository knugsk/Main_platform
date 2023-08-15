<script lang="ts">
    import "./MainPage_Contents.scss";

    import SubNav_ProjectNav from "@/components/SubNav_ProjectNav.svelte";
    
    export let params: { contents_id: string } = { contents_id: "" }
</script>

<div class="container_contents">
    {#if params.contents_id !== "notice"}
        <SubNav_ProjectNav />
    {/if}
    <p>{params.contents_id}</p>
</div>

