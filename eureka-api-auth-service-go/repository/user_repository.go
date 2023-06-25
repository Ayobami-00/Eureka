package repository

import (
	"context"
	"errors"
	"time"

	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/bootstrap"
	"github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/domain"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

const (
	emailIndexName = "EmailIndex"
)

type userRepository struct {
	Db        bootstrap.Database
	TableName string
	Timeout   time.Duration
}

type UserRepository interface {
	Create(ctx context.Context, user *domain.User) error
	Fetch(ctx context.Context) ([]domain.User, error)
	GetByEmail(ctx context.Context, email string) (domain.User, error)
	GetByID(ctx context.Context, id string) (domain.User, error)
}

func NewUserRepository(db bootstrap.Database, timeout time.Duration, tableName string) UserRepository {
	return &userRepository{
		Db:        db,
		TableName: tableName,
		Timeout:   timeout,
	}
}

func (ur *userRepository) Create(ctx context.Context, user *domain.User) error {

	ctx, cancel := context.WithTimeout(ctx, ur.Timeout)
	defer cancel()

	item, err := dynamodbattribute.MarshalMap(user)

	if err != nil {
		return err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(ur.TableName),
		Item:      item,
		ExpressionAttributeNames: map[string]*string{
			"#id": aws.String("id"),
		},
		ConditionExpression: aws.String("attribute_not_exists(#id)"),
	}

	if _, err := ur.Db.Client.PutItemWithContext(ctx, input); err != nil {

		if _, ok := err.(*dynamodb.ConditionalCheckFailedException); ok {
			return err
		}

		return err
	}

	return nil

}

func (ur *userRepository) Fetch(ctx context.Context) ([]domain.User, error) {

	ctx, cancel := context.WithTimeout(ctx, ur.Timeout)
	defer cancel()

	input := &dynamodb.ScanInput{
		TableName: aws.String(ur.TableName),
	}

	res, err := ur.Db.Client.ScanWithContext(ctx, input)

	if err != nil {

		return nil, err
	}

	users := []domain.User{}

	if err := dynamodbattribute.UnmarshalListOfMaps(res.Items, &users); err != nil {

		return users, err
	}

	return users, nil

}

func (ur *userRepository) GetByEmail(ctx context.Context, email string) (domain.User, error) {

	ctx, cancel := context.WithTimeout(ctx, ur.Timeout)
	defer cancel()

	input := &dynamodb.QueryInput{
		TableName:              aws.String(ur.TableName),
		IndexName:              aws.String(emailIndexName),
		KeyConditionExpression: aws.String("email = :email"),
		ExpressionAttributeValues: map[string]*dynamodb.AttributeValue{
			":email": {S: aws.String(email)},
		},
	}

	var user domain.User

	users := []domain.User{}

	res, err := ur.Db.Client.QueryWithContext(ctx, input)

	if err != nil {
		return user, err
	}

	if err := dynamodbattribute.UnmarshalListOfMaps(res.Items, &users); err != nil {

		return user, err
	}

	if len(users) == 0 {

		return user, errors.New("user doesn't exist")

	}

	user = users[0]

	return user, nil

}

func (ur *userRepository) GetByID(ctx context.Context, id string) (domain.User, error) {

	ctx, cancel := context.WithTimeout(ctx, ur.Timeout)
	defer cancel()

	input := &dynamodb.GetItemInput{
		TableName: aws.String(ur.TableName),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {S: aws.String(id)},
		},
	}

	var user domain.User

	res, err := ur.Db.Client.GetItemWithContext(ctx, input)

	if err != nil {
		return user, err
	}

	if res.Item == nil {
		return user, err
	}

	if err := dynamodbattribute.UnmarshalMap(res.Item, &user); err != nil {

		return user, err
	}

	return user, nil

}
