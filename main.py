
# TO DO: import modules
import socket
import random
import dal
# TO DO: set constants
IP = '0.0.0.0'
PORT = 565
SOCKET_TIMEOUT = 0.1
RAND_REQ = "GET RAND"
ERROR = "-1".encode()
#runningid = 1
RANGE = 10 #radius

def main():
    # Open a socket and loop forever while waiting for clients
    dal.defrunning(100)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        try:
            handle_client(client_socket)
        except:
            continue


def get_client_data(client_socket):
    return client_socket.recv(1024).decode()


def handle_client(client_socket):
    while True:
        try:
            client_req_data = get_client_data(client_socket)
        except socket.timeout:
            continue
        print(client_req_data)
        lista = client_req_data.split("$")
        request_type = lista[0]
        if request_type == "REG":
            name = lista[1]
            ip = lista[2]
            longitude = lista[3]
            latitude = lista[4]
            newID = dal.getRunning()
            addCustomer(name, ip, newID, longitude, latitude)
            client_socket.send(str(newID).encode())
            client_socket.close()
        elif request_type == "HELP":
            longitude = lista[1]
            latitude = lista[2]
            nearVolantier(longitude, latitude)
            client_socket.close()
        elif request_type == "HereIsLocation":
            vol_id = lista[1]
            new_ip = lista[2]
            longitude = lista[3]
            latitude = lista[4]
            update_vol(vol_id, new_ip, longitude, latitude)
        elif request_type == "UPD":
            volId = lista[1]
            name = lista[2]
            ip = lista[3]
            longitude = lista[4]
            latitude = lista[5]
            update_vol(name,volId,ip,longitude,latitude)
            client_socket.close()

def update_vol(name, vol_id, new_ip, logitude, latitude):
    dal.delete_vol(vol_id)
    addCustomer(name, new_ip, vol_id, logitude, latitude)


def nearVolantier(longitude, latitude):
    for x in dal.getAllId():
        vol_latitude = dal.GetVolLat(x)
        vol_longitude = dal.GetVolLong(x)
        if 0 < dal.Get_Distance(float(longitude), float(latitude), float(vol_longitude), float(vol_latitude)) < RANGE*RANGE:
            try:
                volunteer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("conecting to " + x)
                volunteer_socket.connect_ex((dal.GetVolIP(x), 600))
                print("conected")
                volunteer_socket.send(("Help$" + latitude + "$" + longitude).encode())
                print("sent")
                volunteer_socket.close()
                print("close")
            except:
                print("conection loss")
                continue

        client_socket, client_address = volunteer_socket.accept()


def addCustomer(name, ip, newID, longitude, latitude):
    file = open("Customers.txt", 'a')
    print(name + " " + ip)
    content = str(newID) + " " + str(name) + " " + str(ip) + " " + str(longitude) + " " + str(latitude) + "\n"
    file.write(content)



if __name__ == "__main__":
    # Call the main handler function
    main()