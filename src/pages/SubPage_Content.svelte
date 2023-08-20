<script lang="ts">
    import "./SubPage_Content.scss";

    import { afterUpdate, onMount } from "svelte";
    import { get_content } from "query";
    import { pop, replace } from "svelte-spa-router";
    import { deflateRaw } from "zlib";
    import axios from "axios";

    import { post_comment, post_comment_child, delete_comment, modify_comment, delete_content, modify_file, delete_file, download_file, type IAuthor, type IComment, type IFile, type IPost } from "query";

    export let params: { content_id: string } = { content_id: "" };

    let data: IPost = null;
    let comment_text = "";

    let is_child_comment: string = "0";
    let is_modify = false;
    let modify_id = "0";
    let body = "";

    let num_child_comment = {};

    const get_data = async (content_id: string) => {
        get_content(content_id)
            .then(res => {
                num_child_comment = {};
                if(data !== null || data !== undefined) data = res;
                data.comments.forEach((comment) => {
                    num_child_comment[comment.id] = 0;
                    if(comment.parent_comment) {
                        num_child_comment[comment.parent_comment] += 1;
                    }
                });
            }).catch(err => {
                console.log(err);
            });
    }

    get_data(params.content_id);

    function filterImages(arr: any) {
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

    async function uploadFiles() {
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.multiple = true;
        fileInput.addEventListener("change", handleFileChange);
        fileInput.click();
    }

    async function handleFileChange(event) {
        const files = event.target.files;

        await modify_file(params.content_id, files).then(b => {
            if(b) get_data(params.content_id);
        });
    }
</script>

<div class="container_content">
    {#if data !== null && data !== undefined &&
        data.comments !== null && data.comments !== undefined
    }
        <div class="container_left">
            <button class="nav_content" on:click={() => {pop();}}>
                <p class="text_titleOrAuthor">{"< 뒤로가기"}</p>
            </button>
            <div class="board_files">
                <p class="text_info_board_files">누르고 다운받으세요!</p>
                {#each filterNonImageFiles(data.files) as file, index}
                    <button class="box_file" on:click={() => {download_file(extractFileNameFromUrl(file.file));}}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                            <path d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"></path>
                        </svg>
                        <div class="box_file_des">
                            <div class="card_file">
                                <p class="text_name_file">{decodeURIComponent(extractFileNameFromUrl(file.file))}</p>
                            </div>
                        </div>
                        <button class="btn_delete_file" on:click|stopPropagation={async (event) => {
                            event.stopPropagation();
                            await delete_file(file.id).then((b) => {
                                if(b) {
                                    get_data(params.content_id);
                                }
                            });
                        }}>
                            <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                                <path d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"></path>
                            </svg>
                        </button>
                    </button>
                {/each}
                {#each filterImages(data.files) as file, index}
                    <button class="box_file" on:click={() => {download_file(extractFileNameFromUrl(file.file));}}>
                      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                          <path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V158.75l-26.07-26.06a16,16,0,0,0-22.63,0l-20,20-44-44a16,16,0,0,0-22.62,0L40,149.37V56ZM40,172l52-52,80,80H40Zm176,28H194.63l-36-36,20-20L216,181.38V200ZM144,100a12,12,0,1,1,12,12A12,12,0,0,1,144,100Z"></path>
                      </svg>
                      <div class="box_file_des">
                          <div class="card_file">
                              <p class="text_name_file">{decodeURIComponent(extractFileNameFromUrl(file.file))}</p>
                          </div>
                      </div>
                      <button class="btn_delete_file" on:click|stopPropagation={async (event) => {
                          event.stopPropagation();
                          await delete_file(file.id).then((b) => {
                              if(b) {
                                  get_data(params.content_id);
                              }
                          });
                      }}>
                          <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                              <path d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"></path>
                          </svg>
                      </button>
                  </button>
                {/each}
                <button class="box_file center" on:click={async () => {await uploadFiles();}}>
                    <h1>+</h1>
                </button>
            </div>
        </div>
        <div class="board_content">
            <div class="box_main">
                <div class="box_titleAndAuthor">
                    <div class="box_title">
                        <p class="text_titleOrAuthor">{data.title}</p>
                    </div>
                    <div class="box_author">
                        <p class="text_titleOrAuthor">{`${data.author.first_name} ${data.author.last_name}`}</p>
                    </div>
                </div>
                <div class="box_content">
                    <textarea disabled class="box_content_text">
                        {"\n" + data.body}
                    </textarea>
                    <div class="box_content_img">
                        {#each filterImages(data.files) as file, index}
                            <button class="card_img" on:click={() => {newWindowPhoto(file.file)}}>
                                <img src={file.file} alt={index.toString()}/>
                            </button>
                        {/each}
                    </div>
                </div>
                <div class="box_btn_modfiy">
                    <button class="btn_main_modify" on:click={() => {
                        replace(`#/write/${params.content_id}`);
                    }}>
                        <p>수정하기</p>
                    </button>
                    <button class="btn_main_delete" on:click={async () => {
                        await delete_content(params.content_id).then((b) => {
                            if(b) {
                                pop();
                            }
                        });
                    }}>
                        <p>삭제하기</p>
                    </button>
                </div>
            </div>
        </div>
        <div class="board_comment">
            <div class="box_comment">
                {#each data.comments.filter((comment) => comment.parent_comment === null) as comment, index}
                    <button class="card_comment" on:click={() => {
                        if(is_child_comment !== "0") {
                            is_child_comment = is_child_comment === comment.id ? "0" : comment.id;
                            comment_text = "";
                            is_modify = false;
                        } else {
                            is_child_comment = comment.id;
                            comment_text = "";
                            is_modify = false;
                        }
                    }}>
                        <p class="text_comment">
                            {`${comment.author.first_name} ${comment.author.last_name}`}
                        </p>
                        <p class="text_comment">
                            {comment.text}
                        </p>
                        <p class="text_num_child_comment">
                           {num_child_comment[comment.id]}
                        </p>
                        <div class="modify_btn">
                            <button class="btn_svg_comment" on:click|stopPropagation={(event) => {
                                event.stopPropagation();
                                is_modify = true;
                                modify_id = comment.id;
                                comment_text = comment.text;
                            }}>
                                <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                                    <path d="M226.76,69a8,8,0,0,0-12.84-2.88l-40.3,37.19-17.23-3.7-3.7-17.23,37.19-40.3A8,8,0,0,0,187,29.24,72,72,0,0,0,88,96,72.34,72.34,0,0,0,94,124.94L33.79,177c-.15.12-.29.26-.43.39a32,32,0,0,0,45.26,45.26c.13-.13.27-.28.39-.42L131.06,162A72,72,0,0,0,232,96,71.56,71.56,0,0,0,226.76,69ZM160,152a56.14,56.14,0,0,1-27.07-7,8,8,0,0,0-9.92,1.77L67.11,211.51a16,16,0,0,1-22.62-22.62L109.18,133a8,8,0,0,0,1.77-9.93,56,56,0,0,1,58.36-82.31l-31.2,33.81a8,8,0,0,0-1.94,7.1L141.83,108a8,8,0,0,0,6.14,6.14l26.35,5.66a8,8,0,0,0,7.1-1.94l33.81-31.2A56.06,56.06,0,0,1,160,152Z"></path>
                                </svg>
                            </button>
                            <button class="btn_svg_comment" on:click={async () => {
                                await delete_comment(comment.id).then((b) => {
                                    if(b) {
                                        is_child_comment = "0";
                                        get_data(params.content_id);
                                    }
                                });
                            }}>
                                <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                                    <path d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"></path>
                                </svg>
                            </button>
                        </div>
                    </button>
                    {#if is_child_comment === comment.id}
                        {#each data.comments.filter((comment_child) => comment_child.parent_comment !== null) as comment_child, child_index}
                            {#if comment_child.parent_comment == is_child_comment}
                                <div class="box_comment_child">
                                    <div class="index_comment_child">
                                        <p class="text_comment">
                                            {"ㄴ"}
                                        </p>
                                    </div>
                                    <div class="card_comment_child">
                                        <p class="text_comment">
                                            {`${comment_child.author.first_name} ${comment_child.author.last_name}`}
                                        </p>
                                        <p class="text_comment">
                                            {comment_child.text}
                                        </p>
                                        <div class="modify_btn">
                                            <button class="btn_svg_comment" on:click={() => {
                                                is_modify = true;
                                                modify_id = comment_child.id;
                                                comment_text = comment_child.text;
                                            }}>
                                                <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                                                    <path d="M226.76,69a8,8,0,0,0-12.84-2.88l-40.3,37.19-17.23-3.7-3.7-17.23,37.19-40.3A8,8,0,0,0,187,29.24,72,72,0,0,0,88,96,72.34,72.34,0,0,0,94,124.94L33.79,177c-.15.12-.29.26-.43.39a32,32,0,0,0,45.26,45.26c.13-.13.27-.28.39-.42L131.06,162A72,72,0,0,0,232,96,71.56,71.56,0,0,0,226.76,69ZM160,152a56.14,56.14,0,0,1-27.07-7,8,8,0,0,0-9.92,1.77L67.11,211.51a16,16,0,0,1-22.62-22.62L109.18,133a8,8,0,0,0,1.77-9.93,56,56,0,0,1,58.36-82.31l-31.2,33.81a8,8,0,0,0-1.94,7.1L141.83,108a8,8,0,0,0,6.14,6.14l26.35,5.66a8,8,0,0,0,7.1-1.94l33.81-31.2A56.06,56.06,0,0,1,160,152Z"></path>
                                                </svg>
                                            </button>
                                            <button class="btn_svg_comment" on:click={async () => {
                                                await delete_comment(comment_child.id).then((b) => {
                                                    if(b) {
                                                        is_child_comment = "0";
                                                        get_data(params.content_id);
                                                    }
                                                });
                                            }}>
                                                <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256">
                                                    <path d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"></path>
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            {/if}
                        {/each}
                    {/if}
                {/each}
            </div>
            <div class="box_send_comment">
                <textarea class="textarea_comment" bind:value={comment_text}/>
                <button class="btn_send_comment" on:click={async () => {
                    if(is_modify) {
                        await modify_comment(modify_id, params.content_id, comment_text).then(b => {
                            if(b) {
                                is_modify = false;
                                comment_text = "";
                                get_data(params.content_id);
                            }
                        })
                    }
                    else if(is_child_comment !== "0") {
                        await post_comment_child(params.content_id, comment_text, is_child_comment.toString()).then(b => {
                            if(b) {
                                comment_text = "";
                                get_data(params.content_id);
                            }
                        });
                    }
                    else {
                        await post_comment(params.content_id, comment_text).then(b => {
                            if(b) {
                                comment_text = "";
                                get_data(params.content_id);
                            }
                        });              
                    }
                }}>
                    <p class="text_send_comment">{is_modify ? "수정하기" : is_child_comment !== "0" ? "대댓글 달기" : "댓글 달기"}</p>
                </button>
            </div>
        </div>
    {:else}
        <h1>헉 페이지를 못 찾겠어요!</h1>
    {/if}
</div>
