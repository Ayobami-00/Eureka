package usecase

import (
	"context"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/domain"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/repository"
)

type registerUsecase struct {
	userRepository repository.UserRepository
}

type RegisterUsecase interface {
	Create(ctx context.Context, user *domain.User) error
	GetUserByEmail(ctx context.Context, email string) (domain.User, error)
}

func NewRegisterUsecase(userRepository repository.UserRepository) RegisterUsecase {
	return &registerUsecase{
		userRepository: userRepository,
	}
}

func (ru *registerUsecase) Create(ctx context.Context, user *domain.User) error {
	return ru.userRepository.Create(ctx, user)
}

func (ru *registerUsecase) GetUserByEmail(ctx context.Context, email string) (domain.User, error) {
	return ru.userRepository.GetByEmail(ctx, email)
}
