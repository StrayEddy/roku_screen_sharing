' main.brs

sub Main()
    ' URL of the server
    server_url = "http://192.168.0.118:4002" ' Replace with your server details

    ' Create the roScreen outside the loop
    screen = CreateObject("roScreen", true, 1280, 720)
'     screen = CreateObject("roScreen", true)

    while true
        uri = "tmp:/screenshare.jpg"

        ' Make the HTTP request to the server
        response = CreateObject("roUrlTransfer")
        response.SetUrl(server_url)
        code = response.GetToFile(uri)

        bm=CreateObject("roBitmap", uri)
        screen.DrawScaledObject(0,0, 2.0, 2.0, bm)
        screen.SwapBuffers()
    end while
end sub