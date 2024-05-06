class Cell
{
private:
    int value;
    Cell left;
    Cell top;
    Cell prev;
     
public:
    Cell(int value);
    ~Cell();
};

Cell::Cell(int value){

}

Cell::~Cell(){
    
}
