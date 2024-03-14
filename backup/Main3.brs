' main.brs

sub Main()
    ' URL of the server
    server_url = "http://192.168.0.118:4002" ' Replace with your server details

    ' Create the roScreen outside the loop
    screen = CreateObject("roScreen", true)
    screen.SetAlphaEnable(true)
    screen.Clear(&h00000000) 'black, fully transparent alpha
    screen.SwapBuffers()

'     uri = "tmp:/screenshare_video.mp4"
    uri = "https://samplelib.com/lib/preview/mp4/sample-20s.mp4"
    content = {
      Stream: { url : uri }
      StreamFormat: "mp4"
    }
    port = CreateObject("roMessagePort")
    player = CreateObject("roVideoPlayer")
    player.SetDestinationRect(0,0,1920,1080)
    player.SetMessagePort(port)
    player.setContentList(content)
    player.play()

    while true
        msg = wait( 0, port)
    end while
'     while true
'
'         ' Make the HTTP request to the server
'         response = CreateObject("roUrlTransfer")
'         response.SetUrl(server_url)
'         code = response.GetToFile(uri)
'
'         if code = 200
'             print "code 200"
'             player.play()
'             is_video_playing = true
'             while is_video_playing
'                 msg = wait( 10000, port)
'                 if type(msg) = "roVideoPlayerEvent"
'                     if msg.isRequestSucceeded()
'                         is_video_playing = false
'                         print "video finished playing"
'                     end if
'                 end if
'             end while
'         else
'             print "not code 200"
'         end if
'
'     end while
end sub