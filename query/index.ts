import axios from "axios";

import { get } from "svelte/store";
import { access_token, user_id, is_login } from "@/lib/store";

const api_url = import.meta.env.VITE_API_URL;
const api_port = import.meta.env.VITE_API_PORT;
const api = api_url + (api_port === "" ? "" : ":" + api_port);

// Sign
const sign_in = async (stu_id: string, password: string): Promise<boolean> => {
    let frm = new FormData();

    frm.append("stu_id", stu_id);
    frm.append("password", password);

    try {
        const res = await axios.post(api + "/users/login/", frm, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });

        if (res.data.token !== null && res.data.token !== undefined) {
            access_token.set(res.data.token);
            is_login.set(true);
            user_id.set(stu_id);
            return true;
        }
    } catch (err) {
        console.log(err);
    }

    return false;
};
const sign_out = async () => {
    try {
        await axios
            .delete(api + "/users/logout/", {
                headers: {
                    Authorization: "Token " + get(access_token),
                },
            })
            .then((res) => {
                access_token.set("");
                is_login.set(false);
                user_id.set("");
            })
            .catch((err) => {
                console.log(err);
            });
    } catch (err) {
        console.log(err);
    }
};
const sign_up = async (
    first_name: string,
    last_name: string,
    password: string,
    password2: string
) => {
    let frm = new FormData();

    frm.append("stu_id", get(user_id));
    frm.append("first_name", first_name);
    frm.append("last_name", last_name);
    frm.append("password", password);
    frm.append("password2", password2);

    await axios
        .post(api + "/users/register/", frm, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((res) => {})
        .catch((err) => {
            console.log(err);
        });
};

// Mypage
const get_my_info = async () => {
    await axios
        .get(api + "/users/user/" + get(user_id), {
            headers: {
                Authorization: "Token " + get(access_token),
            },
        })
        .then((res) => {})
        .catch((err) => {
            console.log(err);
        });
};

// Contents
export interface IAuthor {
    first_name: string;
    last_name: string;
}

export interface IFile {
    id: string;
    file: string;
    post: string;
}

export interface IComment {
    id: string;
    text: string;
    post: string;
    parent_comment: string;
    author: IAuthor;
}

export interface IPost {
    id: string;
    category: string;
    author: IAuthor;
    title: string;
    body: string;
    files: IFile[];
    comments: IComment[];
    published_date: string;
}

const get_contents = async (contents_id: number): Promise<IPost[]> => {
    try {
        const res = await axios.get(
            api + `/posts/categories/${contents_id}/posts`
        );

        if (res.data !== null && res.data !== undefined) {
            return res.data;
        }
    } catch (err) {
        console.log(err);
    }

    return null;
};

// Content
const get_content = async (content_id: string): Promise<IPost> => {
    try {
        const res = await axios.get(api + `/posts/posts/${content_id}/`);

        if (res.data !== null && res.data !== undefined) {
            return res.data;
        }
    } catch (err) {
        return null;
    }

    return null;
};
const modify_content = async (
    content_id: string,
    title: string,
    content: string,
    category: string
): Promise<boolean> => {
    let frm = new FormData();

    frm.append("title", title);
    frm.append("category", category);
    frm.append("body", content);

    try {
        const res = await axios.patch(api + `/posts/posts/${content_id}`, frm, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};
const delete_content = async (content_id: string): Promise<boolean> => {
    try {
        const res = await axios.delete(api + `/posts/posts/${content_id}/`, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};
const modify_file = async (
    content_id: string,
    files: File[]
): Promise<boolean> => {
    let frm = new FormData();

    frm.append("post", content_id);
    for (let i = 0; i < files.length; i++) {
        frm.append("files", files[i]);
    }

    try {
        const res = await axios.post(api + `/posts/files/${content_id}`, frm, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};
const delete_file = async (file_id: string): Promise<boolean> => {
    try {
        const res = await axios.delete(api + `/posts/files/${file_id}`, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};
const download_file = async (file_name: string): Promise<boolean> => {
    try {
        const res = await axios.get(api + `/posts/files/${file_name}`, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};

// Comment Post
const post_comment = async (post: string, text: string): Promise<boolean> => {
    let frm = new FormData();

    frm.append("post", post);
    frm.append("text", text);

    try {
        const res = await axios.post(api + `/posts/comments/create/`, frm, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        if (res.data !== null && res.data !== undefined) return res.data;

        return null;
    } catch (err) {
        return null;
    }
};
const post_comment_child = async (
    post: string,
    text: string,
    parent_comment: string
): Promise<boolean> => {
    let frm = new FormData();

    frm.append("post", post);
    frm.append("text", text);
    frm.append("parent_comment", parent_comment);

    try {
        const res = await axios.post(
            api + `/posts/comments/${parent_comment}/replies/`,
            frm,
            {
                headers: {
                    Authorization: "Token " + get(access_token),
                    "Content-Type": "multipart/form-data",
                },
            }
        );

        if (res.data !== null && res.data !== undefined) return res.data;

        return null;
    } catch (err) {
        return null;
    }
};
const delete_comment = async (id: string): Promise<boolean> => {
    try {
        const res = await axios.delete(api + `/posts/comments/${id}/`, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};
const modify_comment = async (
    id: string,
    post: string,
    text: string
): Promise<boolean> => {
    let frm = new FormData();

    frm.append("post", post);
    frm.append("text", text);

    try {
        const res = await axios.patch(api + `/posts/comments/${id}/`, frm, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        return true;
    } catch (err) {
        return false;
    }
};

// Post
const post = async (
    title: string,
    content: string,
    category: string,
    files: File[]
): Promise<boolean> => {
    let frm = new FormData();

    frm.append("title", title);
    frm.append("category", category);
    frm.append("body", content);

    for (let i = 0; i < files.length; i++) {
        frm.append("files", files[i]);
    }

    try {
        const res = await axios.post(api + `/posts/posts/`, frm, {
            headers: {
                Authorization: "Token " + get(access_token),
                "Content-Type": "multipart/form-data",
            },
        });

        if (res.data !== null && res.data !== undefined) return res.data;

        return null;
    } catch (err) {
        return null;
    }
};

export {
    sign_in,
    sign_up,
    sign_out,
    get_my_info,
    get_contents,
    get_content,
    modify_content,
    delete_content,
    modify_file,
    delete_file,
    download_file,
    post,
    post_comment,
    post_comment_child,
    delete_comment,
    modify_comment,
};
