package auth

import (
	"fmt"
	"log"

	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/bootstrap"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/pkg/auth/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/utils"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type ServiceClient struct {
	Client pb.AuthServiceClient
}

func InitServiceClient(env *bootstrap.Env) pb.AuthServiceClient {

	var transportOption grpc.DialOption

	if env.AppEnv == "PRODUCTION" {

		tlsCredentials, err := utils.LoadTLSCredentials()
		if err != nil {
			log.Fatal("cannot load TLS credentials: ", err)
		}

		transportOption = grpc.WithTransportCredentials(tlsCredentials)

	} else {

		transportOption = grpc.WithTransportCredentials(insecure.NewCredentials())
	}

	cc, err := grpc.Dial(env.AuthServiceUrl, transportOption)

	if err != nil {
		fmt.Println("Could not connect:", err)
	}

	return pb.NewAuthServiceClient(cc)
}
