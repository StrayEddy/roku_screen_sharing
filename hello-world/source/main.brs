'********** Copyright 2016 Roku Corp.  All Rights Reserved. **********

sub Main()
    ' URL of the server
    server_url = "http://192.168.0.118:4002/stream"

    ' Make the HTTP request to the server
    response = CreateObject("roUrlTransfer")
    response.SetUrl(server_url)
    stream_url = response.GetToString()

    if stream_url = ""
        print "Stream is empty, we going live"
        showLiveMirror()
    else
        print stream_url
        showChannelSGScreen(stream_url)
    end if
end sub


sub playVideo(stream_url)
    newContent = CreateObject("roSGNode", "ContentNode")
    newContent.streams=[{ url : stream_url,
    bitrate : 0,
    contentid : "03",
    quality: true
    }]
    newContent.streamFormat = "hls"
    newContent.maxBandwidth = 2640
    newContent.Live = true

    m.video = m.top.findNode("exampleVideo")
    m.video.content = newContent
    m.video.control = "play"
end sub

sub showChannelSGScreen(stream_url)
    print "i am here: A"
    screen = CreateObject("roSGScreen")
    m.port = CreateObject("roMessagePort")
    screen.setMessagePort(m.port)
    m.top = screen.CreateScene("VideoExample")
    screen.show()

    playVideo(stream_url)

    while(true)
        msg = wait(0, m.port)
        msgType = type(msg)

        if msgType = "roSGScreenEvent"
            if msg.isScreenClosed() then return
        end if
    end while

end sub

sub showLiveMirror()
    ' URL of the server
    server_url = "http://192.168.0.118:4002/live"

    ' Create the roScreen outside the loop
    screen = CreateObject("roScreen", true, 1280, 720)

    while true
        uri = "tmp:/screenshare.jpg"

        ' Make the HTTP request to the server
        response = CreateObject("roUrlTransfer")
        response.SetUrl(server_url)
        response.GetToFile(uri)

        bm=CreateObject("roBitmap", uri)
        screen.DrawScaledObject(0,0, 2.0, 2.0, bm)
        screen.SwapBuffers()
    end while
end sub