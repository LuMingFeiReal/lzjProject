function add_pic_left(news) {  
    var uli = $('<li>');
    uli.attr('class',"am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left");

    var odiv = $('<div>');
    odiv.attr('class',"am-u-sm-4 am-list-thumb");

    var oa = $('<a>');
    oa.attr('href', news['url']);
    
    var pic = $('<img>');
    pic.attr('class', 'left-pic');
    pic.attr('src', news['pic']);
    pic.attr('alt', news['title']);
    
    oa.append(pic);
    odiv.append(oa);
    uli.append(odiv);

    var tdiv = $('<div>');
    tdiv.attr('class'," am-u-sm-8 am-list-main list-main-div");

    var oh3 = $('<h3>');
    oh3.attr('class',"am-list-item-hd list-head-h3");

    var ta = $('<a>');
    ta.attr('href', news['url']);
    ta.attr('class', 'my-title');
    ta.html(news['title']);

    oh3.append(ta);
    tdiv.append(oh3);

    var thdiv = $('<div>');
    thdiv.attr('class',"am-list-item-text author-div");
    thdiv.html(news['name']);
    
    tdiv.append(thdiv);
    uli.append(tdiv);

    // uli.addClass('.am-animation-slide-left');
    return uli;
}

function add_pic_right(news){
    var li1 = $('<li>');
    li1.attr('class',"am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-right");

    var div1 = $('<div>');
    div1.attr('class',"am-u-sm-8 am-list-main list-main-div");

    var h31 = $('<h3>');
    h31.attr('class',"am-list-item-hd");

    var a1 = $('<a>');
    a1.attr('href',news['url']);
    a1.html(news['title']);
    a1.attr('class','my-title');

    var div2 = $('<div>');
    div2.attr('class',"am-list-item-text author-div");
    div2.html(news['name']);

    h31.append(a1);
    div1.append(h31);
    div1.append(div2);
    li1.append(div1);
    
    div3 = $('<div>');
    div3.attr('class',"am-u-sm-4 am-list-thumb");

    a2 = $('<a>');
    a2.attr('href',news['url']);

    img1 = $('<img>');
    img1.attr('class','left-pic');
    img1.attr('src',news['pic']);

    a2.append(img1);
    div3.append(a2);
    li1.append(div3);

    return li1;
}


function horizontal_pic(news_list){
    var ul1 = $('<ul>');
    ul1.attr('data-am-widget',"gallery");
    ul1.attr('class',"am-gallery am-avg-sm-2 am-avg-md-3 am-avg-lg-4 am-gallery-default head_nav");
    ul1.attr('data-am-gallery',"{}");

    news_list.forEach(function(news){ 
        var li1 = $('<li>');

        var div1 = $('<div>');
        div1.attr('class',"am-gallery-item");

        var a1 = $('<a>');
        a1.attr('href',news['url']);

        var img1 = $('<img>');
        img1.attr('src',news['pic']);
        img1.attr('class',"left-pic hor-pic");

        var h31 = $('<h3>');
        h31.attr('class',"pic-wrap-title");
        h31.html(news['title']);

        a1.append(img1);
        a1.append(h31);
        div1.append(a1);
        li1.append(div1);

        ul1.append(li1);
    });

    return ul1;
}					
					
function title_style(title){
    str1 = '<div class="am-list-news-hd am-cf mid-title">';
    str2 = '<a href="javascript:void(0)" class=""></a>';
    str3 = '<h2>'+ title +'</h2>';
    str4 = '<span class="am-list-news-more am-fr">更多 &raquo;</span>';
    str5 = '</a></div>'

    return str1 + str2 + str3 +str5;
}


function home_top_news(news_list){
    str1 = '<li class="am-g am-list-item-desced">';
	str2 = '<a href="'+ news['url'] +'" class="am-list-item-hd ">'+ news['title'] +'</a>';
	str3 = '<div class="am-list-item-text">'+ news['name'] +'</div></li>';
    
    return str1 + str2 + str3;
}