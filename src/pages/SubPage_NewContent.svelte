<script lang="ts">
    import "./SubPage_NewContent.scss";
  
    import { get_content } from "query";
    import { pop, replace } from "svelte-spa-router";
  
    import {
      post_comment,
      post_comment_child,
      delete_comment,
      modify_comment,
      delete_content,
      modify_file,
      delete_file,
      type IPost,
    } from "query";
    import koreantime from "@/lib/datetime";
  
    export let params: { content_id: string } = { content_id: "" };
  
    let data: IPost = null;
    let comment_text = "";
    let comment_text_child = "";
  
    let is_child_comment: string = "0";
    let is_modify = false;
    let modify_id = "0";
  
    let num_child_comment = {};
  
    const get_data = async (content_id: string) => {
      get_content(content_id)
        .then((res) => {
          num_child_comment = {};
          if (data !== null || data !== undefined) data = res;
          data.comments.forEach((comment) => {
            num_child_comment[comment.id] = 0;
            if (comment.parent_comment) {
              num_child_comment[comment.parent_comment] += 1;
            }
          });
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    };
  
    get_data(params.content_id);
  
    function filterImages(arr: any) {
      return arr.filter((item: any) => {
        const lowerCaseItem = item.file.toLowerCase();
        return (
          lowerCaseItem.endsWith(".png") ||
          lowerCaseItem.endsWith(".jpeg") ||
          lowerCaseItem.endsWith(".jpg")
        );
      });
    }
  
    function filterNonImageFiles(arr: any) {
      return arr.filter((item: any) => {
        const lowerCaseItem = item.file.toLowerCase();
        return (
          !lowerCaseItem.endsWith(".png") &&
          !lowerCaseItem.endsWith(".jpeg") &&
          !lowerCaseItem.endsWith(".jpg")
        );
      });
    }
  
    function extractFileNameFromUrl(url) {
      const parts = url.split("/");
      return parts[parts.length - 1];
    }
  
    const newWindowPhoto = (link: string) => {
      window.open(link, "_blank");
    };
  
    async function uploadFiles() {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.multiple = true;
      fileInput.addEventListener("change", handleFileChange);
      fileInput.click();
    }
  
    async function handleFileChange(event) {
      const files = event.target.files;
  
      await modify_file(params.content_id, files).then((b) => {
        if (b) get_data(params.content_id);
      });
  
      await get_data(params.content_id);
    }
  
    async function download_file_real(url: string, file_name: string) {
      const modifiedUrl = `${url}?download=true`;
      const link = document.createElement("a");
      link.href = modifiedUrl;
      link.download = file_name;
      link.style.display = "none";
  
      document.body.appendChild(link);
  
      link.click();
  
      document.body.removeChild(link);
    }
  </script>

<div class="container_content">
    {#if data !== null && data !== undefined && data.comments !== null && data.comments !== undefined}
        <div class="box_back_btn">
            <button class="back_btn" on:click={() => pop()}>
                {"<"}
            </button>
        </div>
        <div class="box_title">
            <p>{data.title}</p>
            <p class="non_title">{data.author.first_name + data.author.last_name + " | " + koreantime(data.published_date)}</p>
        </div>
        <div class="box_content">
            <textarea disabled class="box_content_text">
                {"\n" + data.body}
            </textarea>
            {#if filterImages(data.files).length !== 0}
              <div class="box_img">
                {#each filterImages(data.files) as file, index}
                  <button
                    class="card_img"
                    on:click={() => {
                      newWindowPhoto(file.file);
                    }}
                  >
                    <img src={file.file} alt={index.toString()} />
                  </button>
                {/each}
              </div>
            {/if}
            {#if filterNonImageFiles(data.files).length !== 0}
              <div class="box_files">
                {#each filterNonImageFiles(data.files) as file, index}
                  <button
                    class="box_file"
                    on:click={() => {
                      download_file_real(file.file, extractFileNameFromUrl(file.file));
                    }}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="32"
                      height="32"
                      fill="#000000"
                      viewBox="0 0 256 256"
                    >
                      <path
                        d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"
                      />
                    </svg>
                    <div class="card_file">
                      <p class="text_name_file">
                        {decodeURIComponent(extractFileNameFromUrl(file.file))}
                      </p>
                    </div>
                    <button
                      class="btn_delete_file"
                      on:click|stopPropagation={async (event) => {
                        event.stopPropagation();
                        await delete_file(file.id).then((b) => {
                          if (b) {
                            get_data(params.content_id);
                          }
                        });
                      }}
                    >
                      <svg
                        class="svg"
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        fill="#000000"
                        viewBox="0 0 256 256"
                      >
                        <path
                          d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"
                        />
                      </svg>
                    </button>
                  </button>
                {/each}
              </div>
            {/if}
        </div>
        <div class="box_content_edit">
            <button class="box_content_edit_btn"
                on:click={() => {
                    replace(`#/write/${params.content_id}`);
              }}>{"수정하기"}</button>
            <button class="box_content_edit_btn"
                on:click={async () => {
                    await delete_content(params.content_id).then((b) => {
                    if (b) {
                        pop();
                    }
                    });
              }}>{"삭제하기"}</button>
        </div>
        <div class="box_comment_info">
            <p>{"댓글\t|\t" + `${data.comments.length}개`}</p>
        </div>
        <div class="box_comment">
            {#each data.comments.filter((comment) => comment.parent_comment === null) as comment, index}
                <div class="div_comment">
                  <p class="comment_name">
                    {`${comment.author.first_name}${comment.author.last_name}`}
                  </p>
                  <pre class="text_comment">{comment.text}</pre>
                  <div>
                    <button class="box_content_edit_btn"
                        on:click={() => {
                          if (is_child_comment !== "0") {
                            is_child_comment =
                              is_child_comment === comment.id ? "0" : comment.id;
                            is_modify = false;
                          } else {
                            is_child_comment = comment.id;
                            is_modify = false;
                          }
                      }}>{`${num_child_comment[comment.id]}개의 대댓글 보기`}</button>
                    <button class="box_content_edit_btn"
                      on:click={async () => {
                        await delete_comment(comment.id).then((b) => {
                          if (b) {
                            is_child_comment = "0";
                            get_data(params.content_id);
                          }
                        });
                    }}>{`삭제하기`}</button>
                  </div>
                </div>
                {#if is_child_comment === comment.id}
                  {#each data.comments.filter((comment_child) => comment_child.parent_comment !== null) as comment_child, child_index}
                    {#if comment_child.parent_comment == is_child_comment}
                      <div class="div_comment_child">
                        <p class="comment_name">
                          {`${comment_child.author.first_name}${comment_child.author.last_name}`}
                        </p>
                        <pre class="text_comment">{comment_child.text}</pre>
                        <div>
                          <button class="box_content_edit_btn"
                            on:click={async () => {
                              await delete_comment(comment_child.id).then((b) => {
                                if (b) {
                                  is_child_comment = "0";
                                  get_data(params.content_id);
                                }
                              });
                          }}>{`삭제하기`}</button>
                        </div>
                      </div>
                    {/if}
                  {/each}
                  <textarea class="textarea_comment_child" bind:value={comment_text_child} />
                  <button class="btn_comment_child" on:click={async () => {
                    await post_comment_child(
                      params.content_id,
                      comment_text_child,
                      is_child_comment.toString()
                    ).then((b) => {
                      if (b) {
                        comment_text_child = "";
                        get_data(params.content_id);
                      }
                    });
                  }}>
                    대댓글 달기
                  </button>
                {/if}
            {/each}
            <textarea class="textarea_comment" bind:value={comment_text} />
            <button class="btn_comment" on:click={async () => {
                await post_comment(params.content_id, comment_text).then((b) => {
                  if (b) {
                    comment_text = "";
                    get_data(params.content_id);
                  }
                });
            }}>
              댓글 달기
            </button>
        </div>
    {:else}
        <h1>헉 페이지를 못 찾겠어요!</h1>
    {/if}
</div>