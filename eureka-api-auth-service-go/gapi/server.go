package gapi

import (
	"fmt"
	"log"
	"time"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/bootstrap"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/token"
)

type Server struct {
	pb.UnimplementedAuthServiceServer
	Db         bootstrap.Database
	TokenMaker token.Maker
	Env        *bootstrap.Env
	Timeout    time.Duration
}

// NewServer creates a new gRPC server
func NewServer(env *bootstrap.Env, db bootstrap.Database, timeout time.Duration) (*Server, error) {
	tokenMaker, err := token.NewPasetoMaker(env.TokenSymmetricKey)

	if err != nil {
		log.Fatal("Cannot create token maker: ", err)
		return nil, fmt.Errorf("Cannot create token maker: %w", err)
	}

	server := &Server{
		Db:         db,
		TokenMaker: tokenMaker,
		Env:        env,
		Timeout:    timeout,
	}

	return server, nil
}
