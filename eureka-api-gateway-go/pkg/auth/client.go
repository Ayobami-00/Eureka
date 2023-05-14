package auth

import (
	"fmt"
	"log"

	"github.com/Ayobami-00/Eureka/bootstrap"
	"github.com/Ayobami-00/Eureka/pkg/auth/pb"
	"github.com/Ayobami-00/Eureka/utils"
	"google.golang.org/grpc"
)

type ServiceClient struct {
	Client pb.AuthServiceClient
}

func InitServiceClient(env *bootstrap.Env) pb.AuthServiceClient {

	var transportOption grpc.DialOption

	tlsCredentials, err := utils.LoadTLSCredentials()
	if err != nil {
		log.Fatal("cannot load TLS credentials: ", err)
	}

	transportOption = grpc.WithTransportCredentials(tlsCredentials)

	cc, err := grpc.Dial(env.AuthServiceUrl, transportOption)

	if err != nil {
		fmt.Println("Could not connect:", err)
	}

	return pb.NewAuthServiceClient(cc)
}
