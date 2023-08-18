<script lang="ts">
    import "./SubPage_Content.scss";

    import { afterUpdate, onMount } from "svelte";
    import { get_content } from "query";
    import { pop } from "svelte-spa-router";
    import { deflateRaw } from "zlib";
    import axios from "axios";

    import { post_comment } from "query";

    export let params: { content_id: string } = { content_id: "" }

    let data: any = null;
    let comment = "";

    const get_data = async (content_id: string) => {
        get_content(content_id)
            .then(res => {
                if(data !== null || data !== undefined) data = res;
                console.log(data);
                console.log(data.body);
            }).catch(err => {
                console.log(err);
            });
    }

    $: data = get_data(params.content_id)

    function filterImages(arr: any) {
        console.log(arr);
        return arr.filter((item: any) => {
            const lowerCaseItem = item.file.toLowerCase();
            return lowerCaseItem.endsWith('.png') || lowerCaseItem.endsWith('.jpeg') || lowerCaseItem.endsWith('.jpg');
        });
    }

    function filterNonImageFiles(arr: any) {
        return arr.filter((item: any) => {
            const lowerCaseItem = item.file.toLowerCase();
            return !lowerCaseItem.endsWith('.png') && !lowerCaseItem.endsWith('.jpeg') && !lowerCaseItem.endsWith('.jpg');
        });
    }

    function extractFileNameFromUrl(url) {
        const parts = url.split('/');
        return parts[parts.length - 1];
    }

    const newWindowPhoto = (link: string) => {
        window.open(link, '_blank');
    }

    const downloadFile = async (link: string, filename: string) => {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', link, true);
        xhr.responseType = 'blob';

        xhr.onload = function () {
            if (xhr.status === 200) {
                var blob = xhr.response;
                var blobUrl = window.URL.createObjectURL(blob);

                var link = document.createElement('a');
                link.href = blobUrl;
                link.download = filename;

                var clickEvent = new MouseEvent('click', {
                    view: window,
                    bubbles: true,
                    cancelable: false
                });

                link.dispatchEvent(clickEvent);

                window.URL.revokeObjectURL(blobUrl);
            }
        };

        xhr.send();
    }
</script>

<div class="container_content">
    {#if data !== null && data !== undefined && data.comments !== null && data.comments !== undefined}
        <div class="container_left">
            <button class="nav_content" on:click={() => {pop();}}>
                <p class="text_titleOrAuthor">{"< 뒤로가기"}</p>
            </button>
            <div class="board_files">
                <p class="text_info_board_files">누르고 다운받으세요!</p>
                {#each filterNonImageFiles(data.files) as file, index}
                    <button class="box_file" on:click={() => {downloadFile(file.file, "test.cpp");}}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                            <path d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"></path>
                        </svg>
                        <div class="box_file_des">
                            <div class="card_file">
                                <p class="text_name_file">{extractFileNameFromUrl(file.file)}</p>
                            </div>
                        </div>
                    </button>
                {/each}
                {#each filterImages(data.files) as file, index}
                <button class="box_file" on:click={() => {downloadFile(file.file, "test.cpp");}}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                        <path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V158.75l-26.07-26.06a16,16,0,0,0-22.63,0l-20,20-44-44a16,16,0,0,0-22.62,0L40,149.37V56ZM40,172l52-52,80,80H40Zm176,28H194.63l-36-36,20-20L216,181.38V200ZM144,100a12,12,0,1,1,12,12A12,12,0,0,1,144,100Z"></path>
                    </svg>
                    <div class="box_file_des">
                        <div class="card_file">
                            <p class="text_name_file">{extractFileNameFromUrl(file.file)}</p>
                        </div>
                    </div>
                </button>
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
                    <textarea disabled class="box_content_text">
                        {data.body}
                    </textarea>
                    <div class="box_content_img">
                        {#each filterImages(data.files) as file, index}
                            <button class="card_img" on:click={() => {newWindowPhoto(file.file)}}>
                                <img src={file.file} alt={index.toString()}/>
                            </button>
                        {/each}
                    </div>
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
                            {comment.text}
                        </p>
                    </div>
                {/each}
            </div>
            <div class="box_send_comment">
                <textarea class="textarea_comment" bind:value={comment}/>
                <button class="btn_send_comment" on:click={async () => {
                    await post_comment(params.content_id, comment).then(b => {
                        if(b) {
                            comment = "";
                            get_data(params.content_id);
                        }
                    });
                }}>
                    <p class="text_send_comment">답글 달기</p>
                </button>
            </div>
        </div>
    {:else}
        <h1>헉 페이지를 못 찾겠어요!</h1>
    {/if}
</div>