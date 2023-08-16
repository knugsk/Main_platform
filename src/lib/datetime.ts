const koreantime = (inputDateString: string): string => {
    const inputDate = new Date(inputDateString);

    const koreaTimeOffset = 9 * 60; // 한국 시간대 UTC+9
    const koreaDate = new Date(
        inputDate.getTime() + koreaTimeOffset * 60 * 1000
    );

    const year = koreaDate.getFullYear();
    const month = koreaDate.getMonth() + 1;
    const day = koreaDate.getDate();
    const hours = koreaDate.getHours();
    const minutes = koreaDate.getMinutes();

    const formattedString = `${year}년 ${month}월 ${day}일 ${hours}시 ${minutes}분`;

    return formattedString;
};

export default koreantime;
